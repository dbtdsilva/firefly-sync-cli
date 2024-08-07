
from datetime import datetime
from typing import List

from requests import Session
from .base_api import BaseApi
from ..models.transaction import Transaction
from ..models.transaction_type import TransactionType


class TransactionApi(BaseApi):

    def __init__(self, session: Session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/transactions', token)

    def get_transactions(self, start_date: datetime = None, end_date: datetime = None,
                         transaction_type: TransactionType = None) -> List[Transaction]:
        params = {}
        if start_date:
            params['start'] = start_date.strftime(BaseApi.DATE_FORMAT)
        if end_date:
            params['end'] = end_date.strftime(BaseApi.DATE_FORMAT)
        if transaction_type:
            params['type'] = transaction_type
        params['limit'] = 500
        data = self._internal_get('/', params=params)
        return [Transaction(id=item['id'], **item['attributes']['transactions'][0]) for item in data]

    def store_transaction(self, transaction: Transaction) -> Transaction:
        data = self._internal_post('/', {
            'error_if_duplicate_hash': False,
            'apply_rules': True,
            'fire_webhooks': True,
            'group_title': None,
            'transactions': [transaction.model_dump(exclude_none=True, mode='json')]
        })
        return Transaction(id=data['data']['id'], **data['data']['attributes']['transactions'][0])

    def delete_transaction(self, transaction: Transaction) -> None:
        self._internal_delete(f'{transaction.id}')
