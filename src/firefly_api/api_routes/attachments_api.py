
from requests import session
from .base_api import BaseApi
from ..models.attachment import Attachment
import csv


class AttachmentsApi(BaseApi):

    def __init__(self, session: session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/attachments', token)

    def create_attachment(self, attachment: Attachment, data: bytes) -> Attachment:
        response = self._internal_post('/', attachment.model_dump(exclude_none=True, mode='json'))
        new_attachment = Attachment(id=response['data']['id'], **response['data']['attributes'])
        self._internal_post_with_files(endpoint=f'{new_attachment.id}/upload',
                                       data=AttachmentsApi.__bypass_firefly_mime_detection(data))

        return new_attachment

    @staticmethod
    def __is_csv(data: bytes) -> bool:
        try:
            csv.Sniffer().sniff(str(data))
            return True
        except csv.Error:
            return False

    @staticmethod
    def __bypass_firefly_mime_detection(data: bytes) -> bytes:
        if not AttachmentsApi.__is_csv(data):
            return data
        return b'\n' + data
