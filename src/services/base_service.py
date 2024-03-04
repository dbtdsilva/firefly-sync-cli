from abc import ABC


class BaseService(ABC):

    @staticmethod
    def __get_allowed_input(max_value) -> int | None:
        user_input = None
        while True:
            user_input = input("Please select one of the options (or 's' to skip): ").strip().lower()
            if user_input == 's':
                return None
            elif user_input.isdigit() and int(user_input) >= 0 and int(user_input) <= max_value:
                return int(user_input)
