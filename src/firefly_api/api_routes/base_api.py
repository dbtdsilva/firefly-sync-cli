from abc import ABC
import logging

from requests import Session


class BaseApi(ABC):

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, session: Session, base_url: str, token: str) -> None:
        self.session = session

        self.base_url = base_url
        self.token = token
        self.session.headers.update(self.__default_headers(token))

    def __default_headers(self, token):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def __url(self, endpoint):
        if endpoint == '/':
            return self.base_url
        return f'{self.base_url}/{endpoint}'

    def _internal_get(self, endpoint, params=None):
        response = self.session.get(self.__url(endpoint), params=params)
        return self.__get_all_pages(response)

    def __get_all_pages(self, response):
        if response.status_code != 200:
            logging.error(f'Failed to GET {response.request.url}, received {response.status_code}: {response.json()}')
            response.raise_for_status()
        result = response.json()
        if 'data' not in result:
            return result

        data = result['data']
        while 'links' in result and 'next' in result['links']:
            page_request = self.session.get(result['links']['next'])
            if page_request.status_code != 200:
                logging.error(f'Failed to GET {page_request.request.url}, \
                              received {page_request.status_code}: {page_request.json()}')
                page_request.raise_for_status()
            result = page_request.json()
            data.extend(result['data'])
        return data

    def _internal_post(self, endpoint, json_value=None):
        response = self.session.post(self.__url(endpoint), json=json_value)
        if response.status_code != 200 and response.status_code != 204:
            logging.error(f'Failed to POST {endpoint}, received {response.status_code}: {response.json()}')
            response.raise_for_status()
        return response.json()

    def _internal_post_with_files(self, endpoint, data):
        response = self.session.post(self.__url(endpoint), data=data, headers={
            'Content-Type': 'application/octet-stream',
            'Authorization': f'Bearer {self.token}'
        })
        if response.status_code != 204:
            logging.error(f'Failed to POST {endpoint}, received {response.status_code}: {response.json()}')
            response.raise_for_status()

    def _internal_delete(self, endpoint, params=None):
        response = self.session.delete(self.__url(endpoint), params=params)
        if response.status_code != 204:
            logging.error(f'Failed to DELETE {response.request.url}, received {response.status_code}: {response.json()}')
            response.raise_for_status()
