from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .account_type import AccountType

class Account(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    active: Optional[bool]
    order: Optional[int]
    name: str
    type: AccountType
    account_role: Optional[str]
    currency_id: Optional[str]
    currency_code: Optional[str]
    currency_symbol: Optional[str]
    currency_decimal_places: Optional[int]
    current_balance: Optional[str]
    current_balance_date: Optional[datetime]
    iban: Optional[str]
    bic: Optional[str]
    account_number: Optional[str]
    opening_balance: Optional[str]
    current_debt: Optional[str]
    opening_balance_date: Optional[datetime]
    virtual_balance: Optional[str]
    include_net_worth: Optional[bool]
    credit_card_type: Optional[str]
    monthly_payment_date: Optional[datetime]
    liability_type: Optional[str]
    liability_direction: Optional[str]
    interest: Optional[str]
    interest_period: Optional[str]
    notes: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    zoom_level: Optional[int]
