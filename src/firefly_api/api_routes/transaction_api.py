
from datetime import datetime
from typing import List

from requests import Session
from .base_api import BaseApi
from ..models.transaction import Transaction


class TransactionApi(BaseApi):

    def __init__(self, session: Session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/transactions', token)

    def get_transactions(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        data = self.get('/', params={'start': start_date.strftime(BaseApi.DATE_FORMAT), 
                                     'end': end_date.strftime(BaseApi.DATE_FORMAT)})
        return [Transaction(id=item['id'], **item['attributes']['transactions'][0]) for item in data]

    def store_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        return [ self.store_transaction(transaction) for transaction in transactions ]

    def store_transaction(self, transaction: Transaction) -> Transaction:
        data = self.post('/', {
            'error_if_duplicate_hash': True,
            'apply_rules': True,
            'fire_webhooks': True,
            'group_title': None,
            'transactions': [ transaction.model_dump(exclude_none=True, mode='json') ]
        })
        return Transaction(**data['data']['attributes']['transactions'][0])
        