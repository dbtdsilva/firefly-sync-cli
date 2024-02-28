import logging
from typing import List
from datetime import datetime

from .types.parsed_transaction import ParsedTransaction
from .types.parsed_transaction_type import ParsedTransactionType
from .parser import Parser


class SwisscardCsv(Parser):

    @staticmethod
    def parse(file: str) -> List[ParsedTransaction]:
        data = Parser.read_table_from_csv(file)
        # Now data contains the parsed CSV data
        transactions = []
        for row in data:
            transaction_date = datetime.strptime(row['Transaction date'], '%d.%m.%Y')
            description = row['Description']
            currency = row['Currency']
            amount = float(row['Amount'])
            debit_or_credit = row['Debit/Credit']
            status = row['Status']
            # category = row['Category']

            if status != 'Posted':
                logging.warning(f'Skipping transaction in {file}, it has the status {status}')
            if debit_or_credit == 'Debit':
                transaction_type = ParsedTransactionType.DEBIT
            elif debit_or_credit == 'Credit':
                transaction_type = ParsedTransactionType.CREDIT
                amount = abs(amount)
            else:
                raise Exception(f'Invalid transaction type in {file}: {debit_or_credit}')

            transactions.append(ParsedTransaction(
                type=transaction_type, date=transaction_date, amount=amount,
                description=description, currency_code=currency))
        return transactions
