from datetime import datetime
from typing import List

from .base_service import BaseService
from ..firefly_api.models.account_type import AccountType
from ..firefly_api.api import FireflyApi
import logging


class CategorizationService(BaseService):

    def __init__(self, api: FireflyApi, dry_run: bool) -> None:
        super().__init__(api, dry_run)

    def interactive_categorize(self, start_date: datetime = None, end_date: datetime = None,
                               account_ids: List[str] = []):
        accounts = self.api.accounts.get_accounts(type=AccountType.ASSET)
        categories = self.api.categories.get_categories()

        for account in accounts:
            if len(account_ids) != 0 and account.id not in account_ids:
                continue

            logging.info(f'Getting transactions for account \'{account.name}\'')
            transactions = self.api.accounts.get_account_transactions(
                account_id=account.id,
                start_date=start_date,
                end_date=end_date)

            for transaction in transactions:
                for index, category in enumerate(categories):
                    print(f"{index + 1}. {category.name}", end=', ' if index != len(categories) - 1 else None)
                print(f"Transaction: {transaction.description} | {transaction.amount} {transaction.currency_code} "
                      f"| {transaction.type} | {transaction.date}")

                selected_category_index = BaseService._get_allowed_input(len(categories) - 1)
                selected_category = categories[selected_category_index]
                print(selected_category)
