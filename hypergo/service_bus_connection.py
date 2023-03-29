from abc import ABC, abstractmethod

from hypergo.config import Config
from hypergo.message import Message


class ServiceBusConnection(ABC):
    @abstractmethod
    def consume(self, msg: Message, config: Config) -> None:
        ...

    @abstractmethod
    def send(self, message: Message, topic: str) -> None:
        ...
