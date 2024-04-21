from abc import ABC, abstractmethod
from typing import List


class Parser(ABC):
    @abstractmethod
    def parse(self, page: str) -> List:
        raise NotImplementedError
