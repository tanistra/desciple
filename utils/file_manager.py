# -*- coding: utf-8 -*-

import json
import logging as log
import os
from json import JSONDecodeError
from typing import Dict, Any

TEST_DATA_DIRECTORY = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'test_data')

CONFIG_DIRECTORY = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'configuration')


def load_config_from_json(file_name: str) -> Dict[str, Any]:
    """
    Loads data from json file
    :param file_name: json file name
    :return: json data in dictionary format
    """
    file_path = os.path.join(CONFIG_DIRECTORY, file_name)
    return load_json(file_path)


def load_json(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as config_file:
            json_data = json.load(config_file)
    except FileNotFoundError as e:
        log.error(f"{file_path} does not exist")
        raise e
    except JSONDecodeError as e:
        log.error(f"Json file {file_path} is invalid")
        raise e
    log.info(f"data from {file_path} loaded")
    return json_data
