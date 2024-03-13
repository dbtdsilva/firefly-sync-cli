from datetime import timedelta, datetime
import logging
from typing import Dict, List, Tuple

from .base_service import BaseService

from ..firefly_api.models.transaction import Transaction
from ..firefly_api.models.transaction_type import TransactionType

from ..firefly_api.api import FireflyApi


DEFAULT_AMOUNT_DIFF_PERCENTAGE = 2.0
DEFAULT_DATE_DIFF_DAYS = 3


class TransactionLinkService(BaseService):

    def __init__(self, api: FireflyApi, dry_run: bool) -> None:
        super().__init__(api, dry_run)

    def link_identical_transactions(
            self, start_date: datetime, end_date: datetime,
            amount_diff_percentage: float, date_diff_days: int) -> None:
        identical_transactions = self.__get_identical_transactions_by_source(
            start_date, end_date, amount_diff_percentage, date_diff_days)
        linked_transactions = self.__select_identical_transactions(identical_transactions)

        if len(linked_transactions) == 0 or not TransactionLinkService.__get_yes_or_no_input():
            return

        for src_tx, dst_tx in linked_transactions:
            foreign_currency_id = None if src_tx.currency_id == dst_tx.currency_id else dst_tx.currency_id
            foreign_amount = None if foreign_currency_id is None else dst_tx.amount

            internal_reference = None
            if src_tx.internal_reference is not None or dst_tx.internal_reference is not None:
                internal_reference = ', '.join(filter(None, [src_tx.internal_reference, dst_tx.internal_reference]))
            tags = []
            if src_tx.tags is not None:
                tags.extend(src_tx.tags)
            if dst_tx.tags is not None:
                tags.extend(dst_tx.tags)

            joined_transaction = Transaction(
                source_id=src_tx.source_id,
                destination_id=dst_tx.destination_id,
                description=src_tx.description,
                amount=src_tx.amount,
                currency_id=src_tx.currency_id,
                foreign_currency_id=foreign_currency_id,
                foreign_amount=foreign_amount,
                date=src_tx.date,
                process_date=dst_tx.date,
                type=TransactionType.TRANSFER,
                internal_reference=internal_reference,
                tags=tags)

            logging.info(f'Creating joined transaction at {joined_transaction.date}')
            if not self.dry_run:
                self.api.transactions.store_transaction(joined_transaction)
                self.api.transactions.delete_transaction(src_tx)
                self.api.transactions.delete_transaction(dst_tx)
        logging.info('Finished joining transactions')

    def __get_identical_transactions_by_source(
            self, start_date: datetime = None, end_date: datetime = None,
            amount_diff_percentage: float = DEFAULT_AMOUNT_DIFF_PERCENTAGE,
            date_diff_days: int = DEFAULT_DATE_DIFF_DAYS) -> Dict[Transaction, List[Transaction]]:
        amount_diff_percentage = DEFAULT_AMOUNT_DIFF_PERCENTAGE if amount_diff_percentage is None else amount_diff_percentage
        date_diff_days = DEFAULT_DATE_DIFF_DAYS if date_diff_days is None else date_diff_days
        transactions = self.api.transactions.get_transactions(transaction_type=TransactionType.ALL,
                                                              start_date=start_date,
                                                              end_date=end_date)
        identical_transactions = {}
        for src_tx in transactions:
            for dst_tx in transactions:
                if src_tx.id == dst_tx.id or src_tx.source_id == dst_tx.destination_id:
                    continue

                if src_tx.type != TransactionType.WITHDRAWAL or dst_tx.type != TransactionType.DEPOSIT:
                    continue

                if TransactionLinkService.__percentage_difference(src_tx.amount, dst_tx.amount) > amount_diff_percentage or \
                   dst_tx.date < src_tx.date or abs(src_tx.date - dst_tx.date) > timedelta(days=date_diff_days):
                    continue

                if src_tx in identical_transactions:
                    identical_transactions[src_tx].append(dst_tx)
                else:
                    identical_transactions[src_tx] = [dst_tx]
        return identical_transactions

    def __select_identical_transactions(self, identical_transactions: Dict[Transaction, List[Transaction]]) -> \
            Tuple[Transaction, Transaction]:
        already_linked = set()
        linked_transactions = []
        for src_tx, dst_txs in sorted(identical_transactions.items(), key=lambda item: item[0].date):
            dst_txs.sort(key=lambda tx: (
                abs(src_tx.date - tx.date),
                abs(src_tx.amount - tx.amount)))
            dst_txs = [tx for tx in dst_txs if tx.id not in already_linked]
            if src_tx.id in already_linked or len(dst_txs) == 0:
                logging.info(f'Skipping transaction mapping. Src: {src_tx.source_name} / {src_tx.description}, '
                             f'Dst: {len(dst_txs)}')
                continue

            logging.info(f'Src: {src_tx.date}, {src_tx.source_name}, {src_tx.amount}, {src_tx.description}')
            logging.info('Possible mappings:')
            for i, dst_tx in enumerate(dst_txs):
                logging.info(f'\t{i}: {dst_tx.date}, {dst_tx.destination_name}, '
                             f'{dst_tx.amount}, {dst_tx.description}, {dst_tx.id}')

            read_value = BaseService._get_allowed_input(len(dst_txs) - 1)
            if read_value is not None:
                already_linked.add(src_tx.id)
                already_linked.add(dst_txs[read_value].id)
                linked_transactions.append((src_tx, dst_txs[read_value]))
        return linked_transactions

    @staticmethod
    def __percentage_difference(old_value, new_value):
        return abs(((new_value - old_value) / old_value) * 100)

    @staticmethod
    def __get_yes_or_no_input() -> bool:
        user_input = None
        while True:
            user_input = input("Confirm ('yes' or 'no): ").strip().lower()
            if user_input == 'yes':
                return True
            elif user_input == 'no':
                return False
