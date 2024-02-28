from enum import auto
from strenum import PascalCaseStrEnum


class AttachableType(PascalCaseStrEnum):
    ACCOUNT = auto()
    BUDGET = auto()
    BILL = auto()
    TRANSACTIONAL_JOURNAL = auto()
    PIGGY_BANK = auto()
    TAG = auto()
