from .api_routes.account_api import AccountApi
import requests

class FireflyApi:

    def __init__(self, base_url, token) -> None:
        session = requests.Session()
        self.accounts = AccountApi(session, base_url, token)
