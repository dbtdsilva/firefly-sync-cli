
from requests import session
from .base_api import BaseApi
from ..models.attachment import Attachment


class AttachmentsApi(BaseApi):

    def __init__(self, session: session, base_url: str, token: str) -> None:
        super().__init__(session, f'{base_url}/api/v1/attachments', token)

    def create_attachment(self, attachment: Attachment, file_path: str) -> Attachment:
        data = self.post('/', attachment.model_dump(exclude_none=True, mode='json'))
        new_attachment = Attachment(id=data['data']['id'], **data['data']['attributes'])
        self.post_with_files(f'{new_attachment.id}/upload', data=open(file_path, 'rb'))

        return new_attachment
