# -*- coding: utf-8 -*-

import logging as log
import os

import allure
from appium import webdriver


@allure.step("Create appium driver")
def create_driver(
        config_file: dict, app_dir: str) -> webdriver:
    """Create appium driver with specified desired capabilities
        :param config_file: dictionary with test configuration
        :param app_dir: path to directory with test applications
        :return: appium driver

    """
    desired_caps = {'appiumVersion': config_file['appiumVersion'],
                    'deviceOrientation': config_file['deviceOrientation'],
                    'app': os.path.join(app_dir, config_file['app']),
                    'deviceName': config_file['deviceName'],
                    'platformName': config_file['platformName'],
                    'platformVersion': config_file['platformVersion'],
                    'newCommandTimeout': 600
                    }

    platform = config_file['platformName'].lower()
    if platform == 'ios':
        raise NotImplementedError(
            "iOS tests are not available for this project")
    elif platform == 'android':
        desired_caps['adbExecTimeout'] = 50000
        desired_caps['appPackage'] = config_file['appPackage']
        desired_caps['appActivity'] = config_file['appActivity']
        desired_caps['unicodeKeyboard'] = config_file['unicodeKeyboard']
        desired_caps['resetKeyboard'] = config_file['resetKeyboard']
        desired_caps['automationName'] = 'UiAutomator2'
        if config_file['platformVersion'] == '6.0':
            desired_caps['browserName'] = config_file['browserName']
    else:
        raise KeyError(
            f'Unknown test platform {platform}, please use ios or android')
    environment = config_file["remote"]
    log.info(f'Starting appium driver with caps: \n{desired_caps}')
    return webdriver.Remote(environment, desired_caps)
