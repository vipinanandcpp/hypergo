from abc import ABC, abstractmethod
from typing import Any, Dict, Union


class Secrets(ABC):
    @abstractmethod
    def get(self, key: str) -> Union[str, int, Dict[str, Any]]:
        pass