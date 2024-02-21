from enum import auto
from strenum import LowercaseStrEnum


class AccountType(LowercaseStrEnum):
    ALL = auto()
    ASSET = auto()
    CASH = auto()
    EXPENSE = auto()
    REVENUE = auto()
    SPECIAL = auto()
    HIDDEN = auto()
    LIABILITY = auto()
