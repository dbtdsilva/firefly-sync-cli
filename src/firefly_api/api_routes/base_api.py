from abc import ABC

class BaseApi(ABC):
    
    def __init__(self, session, base_url, token) -> None:
        self.session = session

        self.base_url = base_url
        self.session.headers.update(self._default_headers(token))

    def _default_headers(self, token):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    
    def _url(self, endpoint):
        if endpoint == '/':
            return self.base_url
        return f'{self.base_url}/{endpoint}'

    def get(self, endpoint, params=None):
        print(params)
        response = self.session.get(self._url(endpoint), params=params)
        return self._get_all_pages(response)

    def _get_all_pages(self, request):
        result = request.json()
        data = result['data']
        while 'links' in result and 'next' in result['links']:
            page_request = self.session.get(result['links']['next'])
            print(result['links']['next'])
            result = page_request.json()
            data.extend(result['data'])
        return data

    def post(self, endpoint, data=None, json=None):
        response = self.session.post(self._url(endpoint), data=data, json=json)
        return response

    def put(self, endpoint, data=None, json=None):
        response = self.session.put(self._url(endpoint), data=data, json=json)
        return response

    def delete(self, endpoint, params=None):
        response = self.session.delete(self._url(endpoint), params=params)
        return response
