from abc import ABC, abstractmethod


class Configuration(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        ...
