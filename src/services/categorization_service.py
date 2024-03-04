from datetime import datetime, timedelta

from .base_service import BaseService
from ..firefly_api.models.transaction_type import TransactionType
from ..firefly_api.api import FireflyApi


class CategorizationService(BaseService):

    def __init__(self, api: FireflyApi) -> None:
        super().__init__(api)

    def interactive_categorize(self):
        transactions = self.api.transactions.get_transactions(transaction_type=TransactionType.ALL,
                                                              start_date=datetime.now() - timedelta(days=30))
        categories = self.api.categories.get_categories()

        for transaction in transactions:
            for index, category in enumerate(categories):
                print(f"{index + 1}. {category.name}", end=', ' if index != len(categories) - 1 else None)
            print(f"Transaction: {transaction.description} | {transaction.amount} {transaction.currency_code} "
                  f"| {transaction.type} | {transaction.date}")

            selected_category_index = BaseService.__get_allowed_input(len(categories) - 1)
            selected_category = categories[selected_category_index]
            print(selected_category)
