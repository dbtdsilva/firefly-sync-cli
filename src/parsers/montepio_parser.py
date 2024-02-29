from typing import List
from datetime import datetime

from .types.parsed_transaction import ParsedTransaction
from .types.parsed_transaction_type import ParsedTransactionType
from .parser import Parser


class MontepioParser(Parser):

    @staticmethod
    def parse(file: str) -> List[ParsedTransaction]:
        data = Parser.read_table_from_csv(file, encoding='ISO-8859-1', capitalize=True)
        # Now data contains the parsed CSV data
        transactions = []
        for row in data:
            transaction_date = datetime.strptime(row['Data valor'], '%Y-%m-%d')
            description = row['Descrição']
            currency = row['Moeda'].upper()
            amount = float(row['Importância'].replace('.', '').replace(',', '.'))

            if amount <= 0:
                transaction_type = ParsedTransactionType.DEBIT
                amount = abs(amount)
            else:
                transaction_type = ParsedTransactionType.CREDIT

            transactions.append(ParsedTransaction(
                type=transaction_type, date=transaction_date, amount=amount,
                description=description, currency_code=currency))
        return transactions
