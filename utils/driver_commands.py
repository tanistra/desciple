# -*- coding: utf-8 -*-
import logging as log
import os
import time
from typing import Tuple

import allure
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import ELEMENT


class DriverCommands:

    def __init__(self, driver: webdriver) -> None:
        self.driver: webdriver = driver

    def find_element(self, selector: ELEMENT) -> WebElement:
        """Find element on application view.

            :param selector: tuple (eg. By.ID, 'element/id')
            :return: elements handler
        """
        if self.is_webelement(selector):
            return selector
        else:
            element = self.find_elements(selector)
            if len(element) == 0:
                self.on_exception()
                raise AssertionError(
                    f'Could not locate elements by parameters: {selector}')
            log.debug(f'found element by: {selector}')
            return element[0]

    def find_elements(self, selector: tuple) -> list:
        """Find all element on visible view with selector

            :param selector: elements selector
        """
        elements = self.driver.find_elements(*selector)
        log.debug(f'found {len(elements)} elements')
        return elements

    def click_element(self, element: ELEMENT) -> None:
        """Find element and click on it.

            :param element: tuple (eg. By.ID, 'element/id') or Webelement
        """
        element = self.find_element(element)
        element.click()
        log.debug('Element clicked')

    def fill_in(self, selector: ELEMENT, value: str) -> None:
        """Find element and enter text to the field

            :param selector: tuple (eg. By.ID, 'element/id')
            :param value: text
        """
        element = self.find_element(selector)
        element.clear()
        if len(value) > 0:
            element.send_keys(value)
        log.debug(f'Input field filled')

    def get_text_from_element(self, element: ELEMENT) -> str:
        """Find element and get text from it.

            :param element: tuple (eg. By.ID, 'element/id') or WebElement
            :return: text from element
        """
        element = self.find_element(element)
        return element.text

    def check_elements_text(
            self, element: ELEMENT, expected_text: str) -> None:
        """Find element, get text from it and compare with your expectation.

            :param element: element to get text
            :param expected_text: text to compare with text from element
        """
        element_text = self.get_text_from_element(element)
        assert element_text == expected_text, \
            "Wrong text. Should be '%s' instead of '%s'" % (
                expected_text, element_text)
        log.debug(f'Text: {expected_text} is correct!')

    @staticmethod
    def is_webelement(selector: Tuple[MobileBy, str]) -> bool:
        return selector.__class__.__name__ == 'WebElement'

    def find_child_element_in_parent_element(
            self, parent_element, child_element):
        module = self.find_element(selector=parent_element)
        wait_time = 10
        return WebDriverWait(module, wait_time).until(
            EC.presence_of_all_elements_located(locator=child_element))[0]

    def find_all_child_elements_in_parent_element(
            self, parent_element, child_element):
        module = self.find_element(selector=parent_element)
        wait_time = 10
        return WebDriverWait(module, wait_time).until(
            EC.presence_of_all_elements_located(locator=child_element))

    def get_screenshot(self) -> str:
        """
        take screenshot of the current screen and save it in the screenshot
        directory. Screenshot is saved in PNG format.
        :return: path to file
        """
        name = self.driver.test_name if self.driver.__dict__.get('test_name') \
            else f'screenshot_{time.time()}'
        screenshots_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'screenshots')
        if not os.path.exists(screenshots_dir):
            os.mkdir(screenshots_dir)
        file_name = os.path.join(screenshots_dir, name + '.png')
        try:
            self.driver.save_screenshot(file_name)
            log.info(f"Screenshot saved in {file_name}")
            return file_name
        except Exception:
            log.warning(
                f"An error occurred while trying to take the screenshot")
            return ''

    def on_exception(self):
        screenshot_file = self.get_screenshot()
        if screenshot_file:
            allure.attach.file(screenshot_file)
