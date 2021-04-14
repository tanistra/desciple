# -*- coding: utf-8 -*-
from appium.webdriver.webdriver import WebDriver

from pages.android_selectors import (
    TERMS_AND_CONDITIONS_PAGE as ANDROID_SELECTORS)
from pages.ios_selectors import TERMS_AND_CONDITIONS_PAGE as IOS_SELECTORS
from utils import ANDROID
from utils.driver_commands import DriverCommands
from utils.wait_commands import WaitCommands


class TermsAndConditionPage(DriverCommands):

    def __init__(self, driver: WebDriver, platform: str) -> None:
        super().__init__(driver)
        self.wait = WaitCommands(driver)
        self.terms_selectors = ANDROID_SELECTORS if platform == ANDROID else IOS_SELECTORS  # noqa E501

    def click_on_agree_btn(self) -> None:
        btn = self.wait.wait_for_element_to_be_clickable(
            self.terms_selectors['AGREE_BTN'])
        self.click_element(btn)
