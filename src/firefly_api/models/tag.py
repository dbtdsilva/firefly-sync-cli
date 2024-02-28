from datetime import date as dt
from typing import Optional

from pydantic import BaseModel


class Tag(BaseModel):
    id: str = None
    tag: str
    date: Optional[dt] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    zoom_level: Optional[int] = None
