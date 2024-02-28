from .api_routes.account_api import AccountApi
from .api_routes.transaction_api import TransactionApi
import requests


class FireflyApi:

    def __init__(self, base_url, token) -> None:
        session = requests.Session()
        self.accounts = AccountApi(session, base_url, token)
        self.transactions = TransactionApi(session, base_url, token)
