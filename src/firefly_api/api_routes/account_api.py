from typing import List
from requests import Session
from datetime import datetime

from ..models.transaction import Transaction
from ..models.account_type import AccountType
from ..models.account import Account
from .base_api import BaseApi


class AccountApi(BaseApi):

    def __init__(self, session: Session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/accounts', token)

    def get_accounts(self, type: AccountType):
        data = self._internal_get('/', params={'type': type.value})
        return [Account(id=item["id"], **item['attributes']) for item in data]

    def get_account_transactions(self, account_id: str, start_date: datetime = None,
                                 end_date: datetime = None) -> List[Transaction]:
        params = {}
        if start_date is not None:
            params['start'] = start_date.strftime(BaseApi.DATE_FORMAT)
        if end_date is not None:
            params['end'] = end_date.strftime(BaseApi.DATE_FORMAT)

        data = self._internal_get(f'{account_id}/transactions', params=params)
        return [Transaction(id=item['id'], **item['attributes']['transactions'][0])
                for item in data]
