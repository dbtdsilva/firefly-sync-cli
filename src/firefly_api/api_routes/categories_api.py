
from requests import session
from .base_api import BaseApi
from ..models.category import Category


class CategoriesApi(BaseApi):

    def __init__(self, session: session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/categories', token)

    def get_categories(self):
        data = self._internal_get('/')
        return [Category(id=item['id'], **item['attributes']) for item in data]
