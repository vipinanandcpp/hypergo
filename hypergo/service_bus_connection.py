from abc import ABC, abstractmethod

from hypergo.config import ConfigType
from hypergo.executor import Executor
from hypergo.message import MessageType
from hypergo.storage import Storage


class ServiceBusConnection(ABC):
    def general_consume(self, message: MessageType, config: ConfigType, storage: Storage) -> None:
        executor: Executor = Executor(config, storage)
        for execution in executor.execute(message):
            self.send(execution, config["namespace"])

    @abstractmethod
    def send(self, message: MessageType, namespace: str) -> None:
        ...
