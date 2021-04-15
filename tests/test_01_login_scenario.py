# -*- coding: utf-8 -*-
import allure

from pages.login_page import LoginPage
from pages.splash_page import SplashPage
from pages.terms_and_condition_page import TermsAndConditionPage
from pages.sign_up_page import SignUpPage
from pages.reset_password_page import ResetPasswordPage
from tests.baseTest import BaseTest


class LoginScenario(BaseTest):

    @classmethod
    def setUpClass(cls):
        BaseTest().setUpClass()
        cls.splash_page = SplashPage(cls.driver, cls.PLATFORM)
        cls.terms_page = TermsAndConditionPage(cls.driver, cls.PLATFORM)
        cls.login_page = LoginPage(cls.driver, cls.PLATFORM)
        cls.sign_up_page = SignUpPage(cls.driver, cls.PLATFORM)
        cls.reset_page = ResetPasswordPage(cls.driver, cls.PLATFORM)
        cls.splash_page.click_on_get_started_btn()
        cls.terms_page.click_on_agree_btn()
        cls.sign_up_page.switch_to_log_in_page()

    @allure.title("Test 01 - Check if logo is visible on the login page")
    def test_01_check_logo(self):
        self.login_page.is_logo_visible()

    @allure.title("Test 02 - Check if app name is visible on the login page")
    def test_02_check_app_name(self):
        self.login_page.is_app_name_visible()

    @allure.title("Test 03 - Check if login page title  is visible")
    def test_03_check_page_title(self):
        self.login_page.check_page_title()

    @allure.title("Test 04 - Try to log in with empty data")
    def test_04_try_to_log_in_with_empty_data(self):
        self.login_page.click_on_login()
        self.login_page.check_page_title()

    @allure.title("Test 05 - Switch to login page")
    def test_05_try_to_log_in_with_invalid_data(self):
        login = "blah@blah.com"
        password = 'a'*11
        self.login_page.type_login(login)
        self.login_page.type_password(password)
        self.login_page.click_on_login()
        self.login_page.check_page_title()

    @allure.title("Test 06 - Check reset password link")
    def test_06_check_reset_password_link(self):
        self.login_page.click_of_forgot_password()
        self.reset_page.wait_for_page_loaded()
