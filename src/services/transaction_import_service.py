from types import ModuleType
from typing import Tuple
from datetime import datetime, date as dt
import re
import os
import logging
import importlib
import hashlib

from ..firefly_api.models.attachment import Attachment
from ..firefly_api.models.attachable_type import AttachableType
from ..firefly_api.models.tag import Tag
from ..firefly_api.models.transaction import Transaction
from ..firefly_api.models.transaction_type import TransactionType
from ..parsers.types.parsed_transaction import ParsedTransaction
from ..parsers.types.parsed_transaction_type import ParsedTransactionType

from ..firefly_api.api import FireflyApi
from ..firefly_api.models.account_type import AccountType
from ..firefly_api.models.account import Account
from ..parsers.parser import Parser


class TransactionImportService:

    def __init__(self, api: FireflyApi) -> None:
        self.api = api

    def import_file(self, file: str) -> bool:
        logging.info(f'Importing file "{file}"')
        account, parser_module = self.__find_account_matching_file(file)
        if account is None:
            logging.warning(f'Failed to find a valid account for file "{file}"')
            return False
        elif parser_module is None:
            logging.warning(f'Failed to find load parser module for file "{file}" with account "{account.name}"')
            return False

        parsed_transactions = parser_module.parse(file)
        if len(parsed_transactions) == 0:
            logging.info(f'Finished importing file "{file}" earlier, it had no transactions')
            return True

        start_date = min(t.date for t in parsed_transactions)
        end_date = max(t.date for t in parsed_transactions)
        stored_transactions = self.api.accounts.get_account_transactions(
            account_id=account.id, start_date=start_date, end_date=end_date)

        stored_transactions_by_reference = {t.internal_reference: t for t in stored_transactions
                                            if t.internal_reference is not None}

        tag = self.__create_tag_for_import(file, account, start_date, end_date) if not self.dry_run else None

        imported_transactions = []
        for parsed_transaction in parsed_transactions:
            if parsed_transaction.amount == 0:
                logging.warning(f'Parsed transaction had an amount of 0. Parsed: {parsed_transaction}')
                continue
            transaction = self.__map_transaction_to_firefly(parsed_transaction, account, tag)
            if transaction.internal_reference in stored_transactions_by_reference:
                found_transaction = stored_transactions_by_reference[transaction.internal_reference]
                logging.warning(f'Parsed transaction was already stored with id {found_transaction.id} '
                                f'(reference: {found_transaction.internal_reference}). Parsed: {parsed_transaction}')
                continue
            imported_transactions.append(transaction)

        if not self.dry_run:
            self.api.transactions.store_transactions(imported_transactions)
        logging.info(f'Finished importing file "{file}" with {len(imported_transactions)} transactions '
                     f'(parsed {len(parsed_transactions)} transactions)')
        return True

    def __find_account_matching_file(self, file: str) -> Tuple[Account, ModuleType]:
        file_basename = os.path.basename(file)
        accounts = self.api.accounts.get_accounts(AccountType.ASSET)

        match = None
        for account in accounts:
            pattern = r"sync:\s*([^,]+),([^,\n]+)\s*$"
            sync_note = re.search(pattern, account.notes, re.MULTILINE)
            if not sync_note:
                logging.warning(f'Skipping account match, no notes with sync: {accounts[0].name}')
                continue

            match_filename = sync_note.group(1).strip()
            match_parser_module = sync_note.group(2).strip()
            if file_basename.startswith(match_filename) and (match is None or len(match[0]) < match_filename):
                match = (match_filename, account, match_parser_module)
        return (match[1], self.__retrieve_module(match[2])) if match is not None else (None, None)

    def __retrieve_module(self, module) -> Parser:
        try:
            loaded_module = importlib.import_module(f'.parsers.{module}', __package__)
            for _, obj in vars(loaded_module).items():
                if isinstance(obj, type) and issubclass(obj, Parser) and obj != Parser:
                    return obj
            return None
        except ModuleNotFoundError:
            return None

    def __map_transaction_to_firefly(self, parsed_transaction: ParsedTransaction, account: Account, tag: Tag) -> Transaction:
        default_unknown_account = "Unidentified"
        if parsed_transaction.type == ParsedTransactionType.DEBIT:
            transaction_type = TransactionType.WITHDRAWAL
            source_name = account.name
            destination_name = default_unknown_account
        elif parsed_transaction.type == ParsedTransactionType.CREDIT:
            transaction_type = TransactionType.DEPOSIT
            source_name = default_unknown_account
            destination_name = account.name

        currency_code = account.currency_code if parsed_transaction.currency_code is None else \
            parsed_transaction.currency_code
        internal_reference = self.__generate_hash_for_transaction(parsed_transaction)

        return Transaction(
            source_name=source_name,
            destination_name=destination_name,
            description=parsed_transaction.description,
            amount=parsed_transaction.amount,
            date=parsed_transaction.date,
            currency_code=currency_code,
            type=transaction_type,
            internal_reference=internal_reference,
            tags=[tag.tag] if tag is not None else [])

    def __generate_hash_for_transaction(self, parsed_transaction: ParsedTransaction) -> str:
        data = (f"{parsed_transaction.type},{parsed_transaction.date},{parsed_transaction.amount},"
                f"{parsed_transaction.description},{parsed_transaction.currency_code}")
        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()

    def __create_tag_for_import(self, file: str, account: Account, start_date: datetime, end_date: datetime) -> Tag:
        tag = self.api.tags.create_tag(Tag(
            tag=f'import_{account.id}_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}',
            date=dt.today(),
            description=f'Imported file "{file}" to the account "{account.name}" (from {start_date} to {end_date})'))

        self.api.attachments.create_attachment(
            attachment=Attachment(filename=os.path.basename(file), attachable_type=AttachableType.TAG, attachable_id=tag.id),
            file_path=file)
        return tag
