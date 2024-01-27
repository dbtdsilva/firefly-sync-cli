from enum import auto
from strenum import StrEnum

class AccountType(StrEnum):
    ALL = auto()
    ASSET = auto()
    CASH = auto()
    EXPENSE = auto()
    REVENUE = auto()
    SPECIAL = auto()
    HIDDEN = auto()
    LIABILITY = auto()