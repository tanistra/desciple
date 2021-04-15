# -*- coding: utf-8 -*-
import allure
from appium.webdriver.webdriver import WebDriver

from pages.android_selectors import RESET_PASSWORD_PAGE as ANDROID_SELECTORS
from pages.ios_selectors import RESET_PASSWORD_PAGE as IOS_SELECTORS
from utils import ANDROID
from utils.wait_commands import WaitCommands
from utils.driver_commands import DriverCommands


class ResetPasswordPage(DriverCommands):

    def __init__(self, driver: WebDriver, platform: str) -> None:
        super().__init__(driver)
        self.wait = WaitCommands(driver)
        self.reset_page = ANDROID_SELECTORS if platform == ANDROID else IOS_SELECTORS  # noqa E501

    @allure.step('Wait for reset password page is loaded')
    def wait_for_page_loaded(self):
        self.wait.wait_for_element_visibility(
            self.reset_page['RESET_PASSWORD'])
