# -*- coding: utf-8 -*-
from . import SELECTOR, MobileBy


SPLASH_SCREEN: SELECTOR = {
    "GET_STARTED_BTN": (MobileBy.ID, 'getstarted')
}

TERMS_AND_CONDITIONS_PAGE: SELECTOR = {
    "AGREE_BTN": (MobileBy.ID, 'getstarted')
}


LOGIN_SIGNIN_PAGE: SELECTOR = {
    'LOGO': (
        MobileBy.XPATH,
        '//android.widget.LinearLayout[1]/android.widget.ImageView'),
    'APP_NAME': (MobileBy.ID, 'app_name'),
    'PAGE_TITLE': (MobileBy.ID, 'login_register_title'),
    'LOGIN_INPUT': (MobileBy.ID, 'reg_email'),
    'PASSWORD_INPUT': (MobileBy.ID, 'reg_password'),
    'SIGN_IN_BTN': (MobileBy.ID, 'sign_up_p_sign_up_button'),
    'SWITCH_TO_LOG_IN_BTN': (MobileBy.ID, 'sign_up_p_log_in_button'),
    'LOGIN_BTN': (MobileBy.ID, 'sign_up_p_sign_up_button')
}
