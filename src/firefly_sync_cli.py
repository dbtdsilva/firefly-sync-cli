import logging
from typing import Any

from .firefly_api.api import FireflyApi
from .utils.env_mapper import EnvMapper
from .services.categorization_service import CategorizationService
from .services.transaction_import_service import TransactionImportService
from .services.transaction_link_service import TransactionLinkService


class FireflySyncCli:

    MANDATORY_ENV_KEYS = {
        "FIREFLY_URL": "http://localhost:8080",
        "FIREFLY_TOKEN": None
    }

    def __init__(self, dry_run: bool) -> None:
        env_values = EnvMapper(FireflySyncCli.MANDATORY_ENV_KEYS)
        self.api = FireflyApi(env_values.get("FIREFLY_URL"), env_values.get("FIREFLY_TOKEN"))
        self.dry_run = dry_run

    def create_cron_job(self, cli_token) -> Any:
        data = self.api.cron.create_cron_job(cli_token)
        logging.info(f'Cron job run sucessfully: {data}')

    def categorize(self):
        CategorizationService(self.api).interactive_categorize()

    def import_file(self, file: str) -> bool:
        return TransactionImportService(self.api).import_file(file=file)

    def link_identical_transactions(self) -> None:
        TransactionLinkService(self.api).link_identical_transactions()
