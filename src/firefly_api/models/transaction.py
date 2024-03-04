from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from .transaction_type import TransactionType


class Transaction(BaseModel):
    id: str = None
    type: TransactionType
    date: datetime
    amount: float
    description: str
    order: Optional[int] = None
    currency_id: Optional[int] = None
    currency_code: Optional[str] = None
    foreign_amount: Optional[float] = None
    foreign_currency_id: Optional[int] = None
    foreign_currency_code: Optional[str] = None
    budget_id: Optional[int] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    source_id: Optional[int] = None
    source_name: Optional[str] = None
    destination_id: Optional[int] = None
    destination_name: Optional[str] = None
    reconciled: Optional[bool] = None
    piggy_bank_id: Optional[int] = None
    piggy_bank_name: Optional[str] = None
    bill_id: Optional[int] = None
    bill_name: Optional[str] = None
    tags: List[str] = []
    notes: Optional[str] = None
    internal_reference: Optional[str] = None
    external_id: Optional[str] = None
    external_url: Optional[str] = None
    bunq_payment_id: Optional[int] = None
    sepa_cc: Optional[str] = None
    sepa_ct_op: Optional[str] = None
    sepa_ct_id: Optional[str] = None
    sepa_db: Optional[str] = None
    sepa_country: Optional[str] = None
    sepa_ep: Optional[str] = None
    sepa_ci: Optional[str] = None
    sepa_batch_id: Optional[str] = None
    interest_date: Optional[datetime] = None
    book_date: Optional[datetime] = None
    process_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    invoice_date: Optional[datetime] = None

    def __hash__(self) -> int:
        return self.id.__hash__()
