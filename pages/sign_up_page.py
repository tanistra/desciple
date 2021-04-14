# -*- coding: utf-8 -*-
import allure
from appium.webdriver.webdriver import WebDriver

from pages.android_selectors import LOGIN_SIGNIN_PAGE as ANDROID_SELECTORS
from pages.ios_selectors import LOGIN_SIGNIN_PAGE as IOS_SELECTORS
from pages.login_page import LoginPage
from utils import ANDROID
from utils.wait_commands import WaitCommands


class SignUpPage(LoginPage):

    def __init__(self, driver: WebDriver, platform: str) -> None:
        super().__init__(driver, platform)
        self.wait = WaitCommands(driver)
        self.login_selectors = ANDROID_SELECTORS if platform == ANDROID else IOS_SELECTORS  # noqa E501

    @allure.step("Check if 'Sign up' page title is visible")
    def check_page_title(self):
        name = 'Sign up'
        self.check_elements_text(self.login_selectors['PAGE_TITLE'], name)

    @allure.step('Click on the sign in button')
    def click_on_sign_in_btn(self):
        btn = self.wait.wait_for_element_to_be_clickable(
            self.login_selectors['SIGN_IN_BTN'])
        self.click_element(btn)

    @allure.step('Click on the log in button')
    def switch_to_log_in_page(self):
        btn = self.wait.wait_for_element_to_be_clickable(
            self.login_selectors['SWITCH_TO_LOG_IN_BTN'])
        self.click_element(btn)
        super().check_page_title()
