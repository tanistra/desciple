# -*- coding: utf-8 -*-
import base64
import logging
import logging.config
import os
import time
import unittest

import allure
import coloredlogs
from appium import webdriver
from selenium.common.exceptions import WebDriverException

from utils import IOS
from utils.create_driver import create_driver
from utils.file_manager import load_config_from_json


def safe_run(func):

    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error("Test scenario failed on setUpClass")
            logging.error(e)
            self = args[0]()
            self.set_up_failed = True
            self.tearDown()
            self.tearDownClass()
            raise e
    return func_wrapper


class BaseTest(unittest.TestCase):

    coloredlogs.install()
    ROOT_PATH: str = os.path.abspath(
        os.path.dirname(os.path.dirname(__file__)))
    CONFIG_ENV: dict = load_config_from_json('env_config.json')
    APP_DIRECTORY: str = os.path.join(ROOT_PATH, 'test_apps')
    PLATFORM: str = CONFIG_ENV['platformName'].lower()
    MOBILE_FILE = 'android_config.json' if PLATFORM == 'android' else 'ios_config.json'  # noqa E501
    MOBILE_CONFIG = load_config_from_json(MOBILE_FILE)
    driver: webdriver = None
    set_up_failed = False
    recording = False

    @classmethod
    def setUpClass(cls):
        cls.driver = create_driver(cls.MOBILE_CONFIG, cls.APP_DIRECTORY)
        cls.record_screen()

    def setUp(self):
        self.test_name = self.__dict__["_testMethodName"]
        logging.info(f'RUNNING TEST: {self.test_name}')
        self.record_screen()

    def tearDown(self):
        if self.driver and BaseTest.recording:
            try:
                payload = self.driver.stop_recording_screen()
                BaseTest.recording = False
            except WebDriverException:
                logging.error("Unable to stop recording session")
                payload = ''
            if not self.is_failed():
                return
            test_name = self.test_name if hasattr(
                self, 'test_name') else round(time.time() * 1000)
            if payload:
                video_dir = os.path.join('./video', self.PLATFORM)
                video_name = os.path.join(
                    video_dir, f'{test_name}.mp4')
                os.makedirs(video_dir, exist_ok=True)
                with open(video_name, "wb") as fd:
                    fd.write(base64.b64decode(payload))
                logging.info(
                    f"Test failed, recorded move saved to: {video_name}")
                allure.attach.file(
                    source=video_name,
                    name=video_name,
                    attachment_type=allure.attachment_type.MP4)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def is_failed(self):
        if self.set_up_failed:
            return self.set_up_failed
        elif self._outcome.errors:
            return True
        else:
            return False

    @classmethod
    def record_screen(cls):
        if BaseTest.recording:
            logging.debug("Screen recording already in progress")
        else:
            options = {'videoType': 'h264'} \
                if cls.PLATFORM.lower() == IOS else {}
            try:
                cls.driver.start_recording_screen(**options)
                BaseTest.recording = True
            except Exception as e:
                logging.warning('Could not start screen recording')
                logging.warning(e)
