from abc import ABC

from ..firefly_api.api import FireflyApi


class BaseService(ABC):

    def __init__(self, api: FireflyApi, dry_run: bool) -> None:
        self.api = api
        self.dry_run = dry_run

    @staticmethod
    def _get_allowed_input(max_value):
        user_input = None
        while True:
            user_input = input("Please select one of the options (or 's' to skip): ").strip().lower()
            if user_input == 's':
                return None
            elif user_input.isdigit() and int(user_input) >= 0 and int(user_input) <= max_value:
                return int(user_input)
