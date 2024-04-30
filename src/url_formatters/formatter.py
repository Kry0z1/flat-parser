from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, url: str) -> str:
        raise NotImplementedError
