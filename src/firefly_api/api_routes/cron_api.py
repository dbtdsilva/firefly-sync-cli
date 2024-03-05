
from requests import session
from .base_api import BaseApi


class CronApi(BaseApi):

    def __init__(self, session: session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/cron', token)

    def create_cron_job(self, cli_token):
        data = self._internal_get(f'{cli_token}')
        return data
