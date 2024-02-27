import argparse
from types import ModuleType
from typing import Tuple
from dotenv import dotenv_values
import sys
import re
import os
import logging
import importlib


from .firefly_api.api import FireflyApi
from .firefly_api.models.account_type import AccountType
from .firefly_api.models.account import Account
from .firefly_api.models.transaction_type import TransactionType
from .parsers.parser import Parser

__version__ = "1.0.0"

MANDATORY_ENV_KEYS = ["FIREFLY_URL", "FIREFLY_TOKEN"]


class FireflySyncCli:

    def __init__(self) -> None:
        env_values = self.__load_config()
        self.api = FireflyApi(env_values["FIREFLY_URL"], env_values["FIREFLY_TOKEN"])

    def __load_config(self):
        env_values = dotenv_values(".env")
        if not all(mandatory_key in env_values.keys() for mandatory_key in MANDATORY_ENV_KEYS):
            logging.error('Values are missing from .env')
            sys.exit(1)
        return env_values

    # file: montepio_random
    # matches: montepio
    # matches: montepio_random
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

    def import_file(self, file: str):
        account, parser_module = self.__find_account_matching_file(file)
        if account is None:
            logging.warning(f'Failed to find a valid account for file "{file}"')
            return
        elif parser_module is None:
            logging.warning(f'Failed to find load parser module for file "{file}" with account "{account.name}"')
            return
        
        parsed_transactions = parser_module.parse(file)
        print(len(parsed_transactions))

        

        #api.transactions.get_transactions(start_date=datetime.now() - timedelta(days=1000), end_date=datetime.now())

        #transactions = SwisscardCsv.parse_csv('dist/swisscard_november_2023_SC-Transactions_2024-02-21_22-53-33.csv')
        #transactions = BcvParser.parse_excel('dist/bcv_main_TRANSACTIONS LIST [21-02-2024].xlsx')
        #api.transactions.store_transactions(transactions)
