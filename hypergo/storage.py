from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def load(self, file_name: str) -> str:
        pass

    @abstractmethod
    def save(self, file_name: str, content: str) -> None:
        pass
