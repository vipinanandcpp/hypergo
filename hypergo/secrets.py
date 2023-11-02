import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Union


class Secrets(ABC):
    @abstractmethod
    def get(self, key: str) -> Union[str, int, Dict[str, Any]]:
        pass


class LocalSecrets(Secrets):
    def get(self, key: str) -> str:
        return os.environ[key]
