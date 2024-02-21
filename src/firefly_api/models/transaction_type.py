from enum import auto
from strenum import LowercaseStrEnum


class TransactionType(LowercaseStrEnum):
    ALL = auto()
    WITHDRAWAL = auto()
    EXPENSE = auto()
    DEPOSIT = auto()
    INCOME = auto()
    TRANSFER = auto()
    OPENING_BALANCE = auto()
    RECONCILIATION = auto()
    SPECIAL = auto()
    DEFAULT = auto()
