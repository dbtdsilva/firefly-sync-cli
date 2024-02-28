from datetime import datetime

from pydantic import BaseModel, validator
from .parsed_transaction_type import ParsedTransactionType


class ParsedTransaction(BaseModel):
    type: ParsedTransactionType
    date: datetime
    amount: float
    description: str
    currency_code: str

    @validator("*", pre=True, always=True)
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        if v == "":
            return None
        return v
