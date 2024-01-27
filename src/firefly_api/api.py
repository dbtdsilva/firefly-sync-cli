from .api_routes.account_api import AccountApi


class FireflyApi:

    def __init__(self, base_url, token) -> None:
        self.accounts = AccountApi(base_url, token)
