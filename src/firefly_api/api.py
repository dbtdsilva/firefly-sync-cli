from .api_routes.account_api import AccountApi
from .api_routes.attachments_api import AttachmentsApi
from .api_routes.categories_api import CategoriesApi
from .api_routes.cron_api import CronApi
from .api_routes.tags_api import TagsApi
from .api_routes.transaction_api import TransactionApi
import requests


class FireflyApi:

    def __init__(self, base_url, token) -> None:
        session = requests.Session()
        self.accounts = AccountApi(session, base_url, token)
        self.attachments = AttachmentsApi(session, base_url, token)
        self.categories = CategoriesApi(session, base_url, token)
        self.cron = CronApi(session, base_url, token)
        self.tags = TagsApi(session, base_url, token)
        self.transactions = TransactionApi(session, base_url, token)
