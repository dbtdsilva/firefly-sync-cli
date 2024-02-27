from enum import auto
from strenum import LowercaseStrEnum


class ParsedTransactionType(LowercaseStrEnum):
    DEBIT = auto()
    CREDIT = auto()
