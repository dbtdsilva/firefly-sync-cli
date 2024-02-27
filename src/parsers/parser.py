from abc import ABC, abstractmethod
from typing import List

from .types.parsed_transaction import ParsedTransaction


class Parser(ABC):

    @staticmethod
    @abstractmethod
    def parse(file) -> List[ParsedTransaction]:
        pass