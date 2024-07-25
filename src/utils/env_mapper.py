import logging
import sys
from typing import Dict
from dotenv import dotenv_values
import os


class EnvMapper():

    def __init__(self, expected_keys: Dict[str, str] = dict()) -> None:
        self.env_values = self.__load_env_variables(expected_keys)

    def get(self, key) -> str:
        if key not in self.env_values:
            return None
        return self.env_values[key]

    def __load_env_variables(self, expected_keys: Dict[str, str]) -> Dict[str, str]:
        env_values = dotenv_values(".env")
        for expected_key, default_value in expected_keys.items():
            # If the mandatory key exist, then it is all good
            if expected_key in env_values:
                continue

            # Check if it was set in the actual environment and not .env.
            # Otherwise, assign its default value.
            # If there is no default value, throw an error.
            env_value = os.environ.get(expected_key)
            if env_value is not None:
                env_values[expected_key] = env_value
            elif default_value is not None:
                env_values[expected_key] = default_value
            else:
                logging.error(f'Values are missing from environment {expected_key}')
                sys.exit(1)
        return env_values
