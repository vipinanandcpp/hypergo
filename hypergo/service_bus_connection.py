from abc import ABC, abstractmethod

from hypergo.config import Config
from hypergo.executor import Executor
from hypergo.message import Message


class ServiceBusConnection(ABC):
    def general_consume(self, message: Message, config: Config) -> None:
        executor: Executor = Executor(config)
        for execution in executor.execute(message):
            self.send(execution, config.namespace)

    @abstractmethod
    def send(self, message: Message, topic: str) -> None:
        ...
