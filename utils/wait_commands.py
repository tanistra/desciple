# -*- coding: utf-8 -*-
import logging as log
import time
from typing import Tuple, Any, Callable

from appium import webdriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.driver_commands import DriverCommands


class WaitCommands:

    def __init__(self, driver: webdriver) -> None:
        self.wait_time: int = 5
        self.driver: webdriver = driver
        self.commands = DriverCommands(self.driver)
        self.interval: float = 0.5

    def wait_for_element_visibility(
            self, selector: Tuple, wait: float = None) -> WebElement:
        """Wait some time until expected element
         will be visible on current page

            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        log.info(
            f'Waiting {wait} seconds for visibility of element {selector}')
        try:
            element = WebDriverWait(self.driver, wait, poll_frequency=1)\
                .until(EC.visibility_of_element_located(selector))
            return element
        except (TimeoutException, NoSuchElementException):
            self.commands.on_exception()
            raise AssertionError('Could not find element' + str(selector))

    def wait_for_presence_of_element(
            self, selector: Tuple, wait: float = None) -> WebElement:
        """Wait some time until expected element will be presence in DOM

            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        log.info(
            f'Waiting {wait} seconds for visibility of element {selector}')
        try:
            element = WebDriverWait(self.driver, wait)\
                .until(EC.presence_of_element_located(selector))
            return element
        except (TimeoutException, NoSuchElementException):
            self.commands.on_exception()
            raise AssertionError(
                'Element is not located in DOM' + str(selector))

    def wait_for_element_not_visibility(
            self, selector: Tuple, wait: float = None) -> None:
        """Wait some time until expected element will disappear

            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        log.info(f'Waiting {wait} seconds for element {selector} disappear')
        try:
            WebDriverWait(self.driver, wait).until_not(
                EC.visibility_of_all_elements_located(selector))
        except TimeoutException:
            self.commands.on_exception()
            raise AssertionError(
                'Timeout waiting for element disappear' + str(selector))

    def wait_for_expected_text(
            self,
            selector: Any,
            expected_text: str,
            wait=None) -> str:
        """Wait some time until expected text will be visible on current page

            :param selector: element selector
            :param expected_text: text to waiting for
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        log.info(f'Waiting {wait} seconds for text: {expected_text}')
        try:
            if self.commands.is_webelement(selector):
                end_time = time.time() + wait
                while end_time - time.time() >= 0:
                    text = self.commands.get_text_from_element(selector)
                    if text == expected_text:
                        return text
                    time.sleep(0.2)
                else:
                    raise TimeoutException
            else:
                return WebDriverWait(self.driver, wait).until(
                    EC.text_to_be_present_in_element(selector, expected_text))
        except (TimeoutException, NoSuchElementException) as e:
            self.commands.on_exception()
            raise AssertionError(
                f'Something went wrong with reading text from the element: '
                f'\n{str(selector)} '
                f'\n StackTrace: {str(e)}')

    def wait_for_system_alert(self, wait=None):
        """Wait for displaying system alert"""
        wait = wait or self.wait_time
        WebDriverWait(self.driver, wait).until(EC.alert_is_present())

    def wait_for_list_of_elements(self, wait_time, selector: Tuple) -> list:
        for i in range(0, wait_time):
            elements = self.commands.find_elements(selector)
            if len(elements) > 0:
                return elements
            self.wait(1)
        else:
            self.commands.on_exception()
            raise AssertionError(
                "Couldn't find requested elements {}".format(selector)
            )

    def wait_for_element_not_clickable(
            self, selector: Tuple, wait: float = None) -> None:
        """Wait some time until expected element will not be clicable
            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        log.info(f'Waiting {wait} seconds for element {selector} to not be clickable')  # noqa E501
        try:
            WebDriverWait(self.driver, wait).until_not(
                EC.element_to_be_clickable(selector))
        except TimeoutException:
            self.commands.on_exception()
            raise AssertionError(
                'Timeout waiting for element to not be clickable' + str(selector))  # noqa E501

    def wait_for_element_to_be_clickable(
            self, selector: Tuple, wait: float = None) -> WebElement:
        """Wait some time until expected element will not be clicable
            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        log.info(
            f'Waiting {wait} seconds for element {selector} to be clickable')
        try:
            return WebDriverWait(self.driver, wait).until(
                EC.element_to_be_clickable(selector))
        except TimeoutException:
            raise AssertionError(
                'Timeout waiting for element to be clickable' + str(selector))

    def wait_for_condition(
            self,
            predicate: Callable,
            expected_output: Any,
            args: Tuple,
            timeout: int = None,
            interval: float = None) -> Any:
        """
        Waits for some condition to be met
        :param predicate: Callable method
        :param expected_output: output for wait
        :param timeout: time to wait
        :param interval: interval to check predicate
        :param args: callable method arguments
        :return: output from method
        """
        timeout = timeout or self.wait_time
        interval = interval or self.interval
        end_time = time.time() + timeout
        output = None
        while end_time - time.time() >= 0:
            try:
                output = predicate(*args)
                if output == expected_output:
                    return output
            except Exception as e:
                log.warning(f"{e}")
            time.sleep(interval)
        else:
            self.commands.on_exception()
            raise TimeoutException(
                f'Timeout exception waiting for condition current:'
                f' {output},'
                f' expected: {expected_output}')

    def wait_for_condition_not_equal(
            self,
            predicate: Callable,
            unexpected_output: Any,
            args: Tuple[Any],
            timeout: int = None,
            interval: float = None) -> Any:
        """
        Waits for some condition to not be met
        :param predicate: Callable method
        :param unexpected_output: output for compare
        :param timeout: time to wait
        :param interval: interval to check predicate
        :param args: callable method arguments
        :return: output from method
        """
        timeout = timeout or self.wait_time
        interval = interval or self.interval
        end_time = time.time() + timeout
        output = None
        while end_time - time.time() >= 0:
            try:
                if output != predicate(*args):
                    return output
            except Exception as e:
                log.warning(f"{e}")
            time.sleep(interval)
        else:
            self.commands.on_exception()
            raise TimeoutException(
                f'Timeout exception waiting for condition current:'
                f' {output},'
                f' expected: {unexpected_output}')

    @staticmethod
    def wait(sleep_time: float) -> None:
        """
        Sleep for some time
        :param sleep_time: time to sleep
        """
        log.info(f'Sleep time: {sleep_time}')
        time.sleep(sleep_time)
