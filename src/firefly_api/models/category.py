from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    name: str
    notes: Optional[str]
