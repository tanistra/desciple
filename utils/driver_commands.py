# -*- coding: utf-8 -*-
import logging as log
import os
import time
from typing import Tuple, Dict

import allure
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import ELEMENT


class DriverCommands:

    def __init__(self, driver: webdriver) -> None:
        self.driver: webdriver = driver

    def find_element(self, selector: ELEMENT) -> WebElement:
        """Find element on application view.

            :param selector: touple (eg. By.ID, 'element/id')
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
        """Find all elemement on visible view with selector

            :param selector: elements selector
        """
        elements = self.driver.find_elements(*selector)
        log.debug(f'found {len(elements)} elements')
        return elements

    def click_element(self, element: ELEMENT) -> None:
        """Find element and click on it.

            :param element: touple (eg. By.ID, 'element/id') or Webelement
        """
        element = self.find_element(element)
        element.click()
        log.debug('Element clicked')

    def fill_in(self, selector: ELEMENT, value: str) -> None:
        """Find element and enter text to the field

            :param selector: touple (eg. By.ID, 'element/id')
            :param value: text
        """
        element = self.find_element(selector)
        element.clear()
        if len(value) > 0:
            element.send_keys(value)
        log.debug(f'Input field filled')

    def get_text_from_element(self, element: ELEMENT) -> str:
        """Find element and get text from it.

            :param element: touple (eg. By.ID, 'element/id') or WebElement
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

    def swipe_screen(
            self,
            factor_start_x: float,
            factor_end_x: float,
            factor_start_y: float,
            factor_end_y: float,
            duration: int = None) -> None:
        """Use swipe gesture.
            :param factor_start_x - factor x-coordinate at which to start
            :param factor_start_y - factor y-coordinate at which to start
            :param factor_end_x - factor end x-coordinate at which to stop
            :param factor_end_y - factor end y-coordinate at which to stop
            :param duration - (optional) time to take the swipe, in ms.
        """
        start_x = self.get_screen_resolution().get('width', 0)*factor_start_x
        end_x = self.get_screen_resolution().get('width', 0)*factor_end_x
        start_y = self.get_screen_resolution().get('height', 0)*factor_start_y
        end_y = self.get_screen_resolution().get('height', 0)*factor_end_y
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def screen_swiping_up(self) -> None:
        self.swipe_screen(
            factor_start_x=0.5,
            factor_end_x=0.5,
            factor_start_y=0.3,
            factor_end_y=0.7,
            duration=200
        )

    def screen_swiping_down(self, duration: int) -> None:
        self.swipe_screen(
            factor_start_x=0.5,
            factor_end_x=0.5,
            factor_start_y=0.7,
            factor_end_y=0.3,
            duration=duration
        )

    def start_activity(self, app_package: str, app_activity: str) -> None:
        """Android only, Launch app in specified app activity
        :param app_package: Android app package
        :param app_activity: Android app activity to laumch
        """
        self.driver.start_activity(app_package, app_activity)

    def press_on_coordinates(self, x, y):
        """
        tap on screen in specified coordinates
        :param x: x coordiate to press.
        :param y: y coordiate to press.
        """
        TouchAction().press(x=x, y=y)

    def execute_script(self, script, *args):
        self.driver.execute_script(script, *args)
        log.debug(
            "Script {script} has been executed with action {args}".format(
                script=script,
                args=args))

    def get_app_from_background(self, app_package: str, app_activity: str):
        home_button = 3
        self.driver.press_keycode(home_button)
        self.driver.start_activity(
            app_package=app_package,
            app_activity=app_activity)

    def press_mobile_back_button(self) -> None:
        back_button = 4
        self.driver.press_keycode(back_button)

    def press_camera_button(self) -> None:
        camera_button = 27
        self.driver.press_keycode(camera_button)

    def is_webelement(self, selector: Tuple[MobileBy, str]) -> bool:
        return selector.__class__.__name__ == 'WebElement'

    def find_child_element_in_parent_element(
            self, parrent_element, child_element):
        module = self.find_element(selector=parrent_element)
        wait_time = 10
        return WebDriverWait(module, wait_time).until(
            EC.presence_of_all_elements_located(locator=child_element))[0]

    def find_all_child_elements_in_parent_element(
            self, parrent_element, child_element):
        module = self.find_element(selector=parrent_element)
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

    def get_screen_resolution(self) -> Dict:
        """Get connected device screen resolution"""
        return self.driver.get_window_size("handleName")

    def open_ios_app_from_deeplink(
            self, deeplink_selector: ELEMENT, app_selector: ELEMENT) -> None:
        """only for iOS devices to execute view from deeplink"""
        wait = WebDriverWait(self.driver, timeout=10)
        self.driver.execute_script('mobile: pressButton', {'name': 'home'})
        icon = wait.until(EC.visibility_of_element_located(
            locator=deeplink_selector))
        self.click_element(icon)
        self.driver.execute_script('mobile: pressButton', {'name': 'home'})
        app = wait.until(EC.visibility_of_element_located(
            locator=app_selector))
        self.click_element(app)
        self.driver.background_app(3)

    def get_element_attribute(self, element: ELEMENT, attribute: str) -> str:
        """Find element and get attribute of that element."""
        element = self.find_element(element)
        return element.get_attribute(attribute)

    def tab_screen_in_specific_coordinates(
            self, x_multiplicand, y_multiplicand):
        x = self.get_screen_resolution().get('width') * x_multiplicand
        y = self.get_screen_resolution().get('height') * y_multiplicand
        TouchAction(self.driver).tap(x=x, y=y).release().perform()
