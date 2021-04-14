# desciple
Recruitment project


# Requirements:
* Be sure you have properly configured Appium - read more http://appium.io
* Be sure you have installed allure - https://docs.qameta.io/allure/ (can be installed with brew)
* Be sure you have python version > 3.6 installed

# How to run project:
* Put your app to the ./desciple/test_apps directory
* Check project configuration in the ./desciple/configuration/android_config.json file
* execute following commands:

` $ python3 -m venv ./venv`
 
` $ source venv/bin/activate`
 
 `$ pip3 install -r requirements.txt`
 
 `$ pytest -s --alluredir allure-results`
`
# How to generate test report:

`$ allure serve allure-results`



