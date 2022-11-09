import os
import sys
import yaml

from sensor.logger import logging
from sensor.exception import SensorException

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise SensorException(e,sys)
