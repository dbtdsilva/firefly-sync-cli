from types import ModuleType
from typing import Tuple
from dotenv import dotenv_values
from datetime import datetime, date as dt
import sys
import re
import os
import logging
import importlib
import hashlib

from .firefly_api.models.attachment import Attachment
from .firefly_api.models.attachable_type import AttachableType
from .firefly_api.models.tag import Tag
from .firefly_api.models.transaction import Transaction
from .firefly_api.models.transaction_type import TransactionType
from .parsers.types.parsed_transaction import ParsedTransaction
from .parsers.types.parsed_transaction_type import ParsedTransactionType

from .firefly_api.api import FireflyApi
from .firefly_api.models.account_type import AccountType
from .firefly_api.models.account import Account
from .parsers.parser import Parser

__version__ = "1.0.0"

MANDATORY_ENV_KEYS = ["FIREFLY_URL", "FIREFLY_TOKEN"]


class FireflySyncCli:

    def __init__(self) -> None:
        env_values = self.__load_config()
        self.api = FireflyApi(env_values["FIREFLY_URL"], env_values["FIREFLY_TOKEN"])

    def import_file(self, file: str):
        account, parser_module = self.__find_account_matching_file(file)
        if account is None:
            logging.warning(f'Failed to find a valid account for file "{file}"')
            return
        elif parser_module is None:
            logging.warning(f'Failed to find load parser module for file "{file}" with account "{account.name}"')
            return

        parsed_transactions = parser_module.parse(file)
        start_date = min(t.date for t in parsed_transactions)
        end_date = max(t.date for t in parsed_transactions)
        stored_transactions = self.api.accounts.get_account_transactions(
            account_id=account.id, start_date=start_date, end_date=end_date)

        stored_transactions_by_reference = {t.internal_reference: t for t in stored_transactions
                                            if t.internal_reference is not None}

        imported_transactions = []
        for parsed_transaction in parsed_transactions:
            transaction = self.__map_transaction_to_firefly(account, parsed_transaction)
            if transaction.internal_reference in stored_transactions_by_reference:
                found_transaction = stored_transactions_by_reference[transaction.internal_reference]
                logging.warning(f'Parsed transaction was already stored with id {found_transaction.id} \
                                (reference: {found_transaction.internal_reference}). Parsed: {parsed_transaction}')
                continue
            imported_transactions.append(transaction)

        has_duplicate_references = len({obj.internal_reference for obj in imported_transactions}) != len(imported_transactions)
        if has_duplicate_references:
            logging.error(f'Parsed transactions contain duplicated rows, please verify the file {file}')
            return

        self.__create_tag_for_import(file, account, start_date, end_date)

        #print(len(imported_transactions))
        #print(imported_transactions[0])
        # self.api.transactions.store_transactions(imported_transactions)

    def __load_config(self):
        env_values = dotenv_values(".env")
        if not all(mandatory_key in env_values.keys() for mandatory_key in MANDATORY_ENV_KEYS):
            logging.error('Values are missing from .env')
            sys.exit(1)
        return env_values

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

            match_filename = sync_note.group(1)
            match_parser_module = sync_note.group(2)
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

    def __map_transaction_to_firefly(self, account: Account, parsed_transaction: ParsedTransaction) -> Transaction:
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
            internal_reference=internal_reference)

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
