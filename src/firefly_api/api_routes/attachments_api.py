
from requests import session
from .base_api import BaseApi
from ..models.attachment import Attachment


class AttachmentsApi(BaseApi):

    def __init__(self, session: session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/attachments', token)

    def create_attachment(self, attachment: Attachment, data: bytes, mimetype: str) -> Attachment:
        response = self._internal_post('/', attachment.model_dump(exclude_none=True, mode='json'))
        new_attachment = Attachment(id=response['data']['id'], **response['data']['attributes'])
        self._internal_post_with_files(endpoint=f'{new_attachment.id}/upload',
                                       data=AttachmentsApi.__bypass_firefly_mime_detection(data, mimetype),
                                       mimetype=mimetype)
        return new_attachment

    @staticmethod
    def __bypass_firefly_mime_detection(data: bytes, mimetype: str) -> bytes:
        if mimetype != 'text/csv':
            return data
        return b'\n' + data
