
from datetime import datetime
from typing import List
from .base_api import BaseApi
from ..models.transaction import Transaction


class TransactionApi(BaseApi):

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, session, base_url, token) -> None:
        super().__init__(session, f'{base_url}/api/v1/transactions', token)

    def get_transactions(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        data = self.get('/', params={'start': start_date.strftime(TransactionApi.DATE_FORMAT), 
                                     'end': end_date.strftime(TransactionApi.DATE_FORMAT)})
        return [Transaction(**item["attributes"]["transactions"][0]) for item in data]

    def store_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        data = self.post('/', {
            'error_if_duplicate_hash': True,
            'apply_rules': True,
            'fire_webhooks': True,
            'group_title': None,
            'transactions': transactions
        })
        return [Transaction(**item["attributes"]["transactions"][0]) for item in data]
        