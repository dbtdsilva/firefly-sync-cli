from requests import Session
from ..models.account_type import AccountType
from ..models.account import Account
from .base_api import BaseApi


class AccountApi(BaseApi):

    def __init__(self, session: Session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/accounts', token)

    def get_accounts(self, type: AccountType):
        data = self.get('/', params={'type': type.value})
        return [Account(**item['attributes']) for item in data]
