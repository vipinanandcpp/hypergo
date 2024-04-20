from abc import ABC, abstractmethod
from typing import Any, cast

from hypergo.config import ConfigType
from hypergo.executor import Executor
from hypergo.message import MessageType
from hypergo.monitor import collect_metrics
from hypergo.utility import do_cprofile


class Connection(ABC):
    @do_cprofile
    def general_consume(self, message: MessageType, **kwargs: Any) -> None:
        config: ConfigType = kwargs.pop("config")
        executor: Executor = Executor(config, **kwargs)
        self.__send_message(executor=executor, message=message, config=config)

    @collect_metrics
    def __send_message(self, executor: Executor, message: MessageType, config: ConfigType) -> None:
        for execution in executor.execute(message):
            self.send(cast(MessageType, execution), config["namespace"])

    @abstractmethod
    def send(self, message: MessageType, namespace: str) -> None:
        pass
