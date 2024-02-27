from typing import List
from datetime import datetime
import openpyxl
import numbers

from .parser import Parser
from .types.parsed_transaction import ParsedTransaction
from .types.parsed_transaction_type import ParsedTransactionType

class BcvParser(Parser):

    @staticmethod
    def read_table_from_excel(file_path, start_text):
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        # Find the starting row and column of the table
        start_row = None
        start_col = None
        for row in sheet.iter_rows():
            if row[0].value == start_text:
                start_row = row[0].row
                start_col = row[0].column
                break

        if not start_row or not start_col:
            raise ValueError("Could not find table starting with 'Execution date'")

        # Extract headers
        headers = [cell.value for cell in sheet[start_row]]

        # Extract data and convert to dictionaries
        data = []
        for row in sheet.iter_rows():
            if row[0].row <= start_row:
                continue
            data_row = {headers[i]: cell.value for i, cell in enumerate(row)}
            data.append(data_row)

        return data

    @staticmethod
    def parse(file: str) -> List[ParsedTransaction]:
        data = BcvParser.read_table_from_excel(file_path=file, start_text='Execution date')
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