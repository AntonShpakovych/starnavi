import json
from typing import Dict
import jsonschema

from bot.core.readers.schema import SCHEMA


class ConfigReader:
    """Read settings for bot from config file"""
    VALID_SCHEMA = SCHEMA

    def __init__(self, path_to_config: str = "config.json") -> None:
        self.path_to_config = path_to_config

    def handle_config(self) -> Dict[str, int]:
        """Parse config and return data"""
        with open(self.path_to_config, "r") as config_file:
            data = json.load(config_file)

        self.is_config_file_valid(data=data, schema=ConfigReader.VALID_SCHEMA)

        return data

    @staticmethod
    def is_config_file_valid(
            data: Dict[str, int],
            schema: Dict[str, int]
    ) -> None:
        """Validate if given config is valid"""
        jsonschema.validate(data, schema)
