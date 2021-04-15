# -*- coding: utf-8 -*-
import allure
from appium.webdriver.webdriver import WebDriver

from pages.android_selectors import LOGIN_SIGNIN_PAGE as ANDROID_SELECTORS
from pages.ios_selectors import LOGIN_SIGNIN_PAGE as IOS_SELECTORS
from utils import ANDROID
from utils.driver_commands import DriverCommands
from utils.wait_commands import WaitCommands


class LoginPage(DriverCommands):

    def __init__(self, driver: WebDriver, platform: str) -> None:
        super().__init__(driver)
        self.wait = WaitCommands(driver)
        self.login_selectors = ANDROID_SELECTORS if platform == ANDROID else IOS_SELECTORS  # noqa E501

    @allure.step('Check if logo is visible on the login page')
    def is_logo_visible(self) -> None:
        self.wait.wait_for_element_visibility(
            self.login_selectors['LOGO'])

    @allure.step('Check if app name is visible on the login page')
    def is_app_name_visible(self):
        name = 'appiumqatest'
        self.check_elements_text(self.login_selectors['APP_NAME'], name)

    @allure.step("Check if login page title is visible")
    def check_page_title(self):
        name = 'Log In'
        self.check_elements_text(self.login_selectors['PAGE_TITLE'], name)

    @allure.step('Fill in login filed with text {login}')
    def type_login(self, login):
        self.fill_in(self.login_selectors['LOGIN_INPUT'], login)

    @allure.step('Fill in password filed with text {password}')
    def type_password(self, password):
        self.fill_in(self.login_selectors['PASSWORD_INPUT'], password)

    @allure.step('Click on the log in button')
    def click_on_login(self):
        self.click_element(self.login_selectors['LOGIN_BTN'])

    @allure.step('Click on the forgot password link')
    def click_of_forgot_password(self):
        self.click_element(self.login_selectors['FORGOT_PASSWORD_BTN'])
