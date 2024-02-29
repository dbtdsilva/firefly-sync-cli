from typing import List
from datetime import datetime

from .types.parsed_transaction import ParsedTransaction
from .types.parsed_transaction_type import ParsedTransactionType
from .parser import Parser


class WiseParser(Parser):

    @staticmethod
    def parse(file: str) -> List[ParsedTransaction]:
        data = Parser.read_table_from_csv(file)
        # Now data contains the parsed CSV data
        transactions = []
        for row in data:
            transaction_date = datetime.strptime(row['Date'], '%d-%m-%Y')
            description = row['Description']
            currency = row['Currency'].upper()
            amount = float(row['Amount'])

            if amount <= 0:
                transaction_type = ParsedTransactionType.DEBIT
                amount = abs(amount)
            else:
                transaction_type = ParsedTransactionType.CREDIT

            transactions.append(ParsedTransaction(
                type=transaction_type, date=transaction_date, amount=amount,
                description=description, currency_code=currency))
        return transactions
