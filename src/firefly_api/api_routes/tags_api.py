
from requests import HTTPError, session
from .base_api import BaseApi
from ..models.tag import Tag


class TagsApi(BaseApi):

    def __init__(self, session: session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/tags', token)

    def create_tag(self, tag: Tag) -> Tag:
        existing_tag = self.get_tag(tag)
        if existing_tag is not None:
            return existing_tag

        data = self.__internal_post('/', tag.model_dump(exclude_none=True, mode='json'))
        return Tag(id=data['data']['id'], **data['data']['attributes'])

    def get_tag(self, tag: Tag) -> Tag:
        try:
            data = self.__internal_get(f'{tag.tag}')
            return Tag(id=data['id'], **data['attributes'])
        except HTTPError as error:
            if error.response.status_code == 404:
                return None
            raise
