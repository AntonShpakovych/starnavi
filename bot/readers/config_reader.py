import json
from typing import Dict
import jsonschema

from bot.readers.schema import schema


class ConfigReader:
    """Read settings for bot from config file"""
    VALID_SCHEMA = schema

    def __init__(self, path_to_config: str = "../config.json") -> None:
        self.path_to_config = path_to_config

    def handle_config(self) -> Dict[str, int]:
        with open(self.path_to_config, "r") as config_file:
            data = json.load(config_file)

        self.is_config_file_valid(data=data)

        return data

    @staticmethod
    def is_config_file_valid(data: Dict[str, int]) -> None:
        jsonschema.validate(data, schema)
