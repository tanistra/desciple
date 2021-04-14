# -*- coding: utf-8 -*-
from typing import Union, Tuple
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webelement import WebElement

ELEMENT = Union[WebElement, Tuple[MobileBy, str]]
ANDROID = 'android'
IOS = 'ios'
