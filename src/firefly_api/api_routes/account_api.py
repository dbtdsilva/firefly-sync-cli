import requests

from ..models.account_type import AccountType
from .base_api import BaseApi


class AccountApi(BaseApi):

    def __init__(self, session, base_url, token) -> None:
        super().__init__(session, f'{base_url}/api/v1/accounts', token)

    def get_accounts(self, type: AccountType):
        return self.get('/', params={'type': type.value})
