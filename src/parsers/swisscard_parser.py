import csv
import logging
from typing import List

from ..firefly_api.models.transaction import Transaction

class SwisscardCsv:

    @staticmethod
    def parse_csv(file: str) -> List[Transaction]:
        data = []
        with open(file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)  # Read the header row
            for row in csvreader:
                parsed_row = {header: value for header, value in zip(headers, row)}
                data.append(parsed_row)

        # Now data contains the parsed CSV data
        for row in data:
            transaction_date = row['Transaction date']
            description = row['Description']
            currency = row['Currency']
            amount = row['Amount']
            debit_or_credit = row['Debit/Credit']
            status = row['Status']
            category = row['Category']
            logging.info(f"Transaction: {transaction_date, description, currency, amount, debit_or_credit, status, category}") 
