import requests

from ..models.account_type import AccountType


class AccountApi:

    def __init__(self, base_url, token) -> None:
        self.base_url = base_url + 'api/v1/'
        self.token = token

    def _default_headers(self):
        return {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.token
        }

    def get_accounts(self, type: AccountType):
        url = self.base_url + 'accounts'
        request = requests.get(url, headers=self._default_headers(), params={'type': type.value})
        return self.get_all_pages(request)

    def get_all_pages(self, request):
        result = request.json()
        data = result['data']
        while 'links' in result and 'next' in result['links']:
            page_request = requests.get(result['links']['next'], headers=self._default_headers())
            result = page_request.json()
            data.extend(result['data'])
        return data
