# -*- coding: utf-8 -*-
import allure
from appium.webdriver.webdriver import WebDriver

from pages.android_selectors import SPLASH_SCREEN as ANDROID_SELECTORS
from pages.ios_selectors import SPLASH_SCREEN as IOS_SELECTORS
from utils import ANDROID
from utils.driver_commands import DriverCommands
from utils.wait_commands import WaitCommands


class SplashPage(DriverCommands):

    def __init__(self, driver: WebDriver, platform: str) -> None:
        super().__init__(driver)
        self.wait = WaitCommands(driver)
        self.splash_selectors = ANDROID_SELECTORS if platform == ANDROID else IOS_SELECTORS  # noqa E501

    @allure.step('Click on the get started button')
    def click_on_get_started_btn(self) -> None:
        btn = self.wait.wait_for_element_to_be_clickable(
            self.splash_selectors['GET_STARTED_BTN'])
        self.click_element(btn)
