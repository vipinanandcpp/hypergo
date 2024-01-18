from abc import ABC, abstractmethod
from typing import Any, cast

from hypergo.config import ConfigType
from hypergo.executor import Executor
from hypergo.message import MessageType


class Connection(ABC):
    def general_consume(self, message: MessageType, **kwargs: Any) -> None:
        config: ConfigType = kwargs.pop("config")
        executor: Executor = Executor(config, **kwargs)
        for execution in executor.execute(message):
            self.send(cast(MessageType, execution), config["namespace"])

    @abstractmethod
    def send(self, message: MessageType, namespace: str) -> None:
        ...
