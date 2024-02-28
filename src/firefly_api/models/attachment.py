from typing import Optional
from pydantic import BaseModel

from .attachable_type import AttachableType


class Attachment(BaseModel):
    id: str = None
    filename: str
    attachable_type: AttachableType
    attachable_id: str
    title: Optional[str] = None
    notes: Optional[str] = None
