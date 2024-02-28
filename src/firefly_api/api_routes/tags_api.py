
from requests import session
from .base_api import BaseApi
from ..models.tag import Tag


class TagsApi(BaseApi):

    def __init__(self, session: session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/tags', token)

    def create_tag(self, tag: Tag) -> Tag:
        data = self.post('/', tag.model_dump(exclude_none=True, mode='json'))
        return Tag(id=data['data']['id'], **data['data']['attributes'])