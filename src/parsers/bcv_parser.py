from typing import List
from datetime import datetime
import numbers

from .parser import Parser
from .types.parsed_transaction import ParsedTransaction
from .types.parsed_transaction_type import ParsedTransactionType

class BcvParser(Parser):

    @staticmethod
    def parse(file: str) -> List[ParsedTransaction]:
        data = Parser.read_table_from_excel(file_path=file, start_text='Execution date')
        # Now data contains the parsed CSV data
        transactions = []
        for row in data:
            transaction_date = datetime.strptime(row['Execution date'], '%d.%m.%Y')
            description = row['Transactions']
            debit = row['Debit'] if isinstance(row['Debit'], numbers.Number) else None
            credit = row['Credit'] if isinstance(row['Credit'], numbers.Number) else None

            if (debit is not None and credit is not None) or \
                (debit is None and credit is None):
                raise Exception(f'Invalid debit / credit in {file}')
            elif debit is not None:
                amount = debit
                transaction_type = ParsedTransactionType.DEBIT
            elif credit is not None:
                amount = credit
                transaction_type = ParsedTransactionType.CREDIT

            transactions.append(ParsedTransaction(
                type=transaction_type, amount=amount, description=description,
                date=transaction_date, currency_code='CHF'))
        return transactions