from typing import List

from .types.parsed_transaction import ParsedTransaction
from .types.parsed_transaction_type import ParsedTransactionType
from .parser import Parser


class ActivoBankParser(Parser):

    @staticmethod
    def parse(file: str) -> List[ParsedTransaction]:
        data = Parser.read_table_from_excel(file=file, start_text='Data Lanc.')
        # Now data contains the parsed CSV data
        transactions = []
        for row in data:
            transaction_date = row['Data Valor']
            description = row['Descrição']
            amount = float(row['Valor'])

            if amount <= 0:
                transaction_type = ParsedTransactionType.DEBIT
                amount = abs(amount)
            else:
                transaction_type = ParsedTransactionType.CREDIT

            transactions.append(ParsedTransaction(
                type=transaction_type, date=transaction_date, amount=amount,
                description=description))
        return transactions
