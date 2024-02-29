from datetime import datetime

from pydantic import BaseModel
from .parsed_transaction_type import ParsedTransactionType


class ParsedTransaction(BaseModel):
    type: ParsedTransactionType
    date: datetime
    amount: float
    description: str
    currency_code: str = None
