from abc import ABC, abstractmethod
from typing import Union, cast

from hypergo.config import ConfigType
from hypergo.executor import Executor
from hypergo.message import MessageType
from hypergo.secrets import Secrets
from hypergo.storage import Storage


class Connection(ABC):
    def general_consume(
        self,
        message: MessageType,
        config: ConfigType,
        storage: Union[Storage, None],
        secrets: Union[Secrets, None] = None,
    ) -> None:
        executor: Executor = Executor(config, storage, secrets)
        for execution in executor.execute(message):
            self.send(cast(MessageType, execution), config["namespace"])

    @abstractmethod
    def send(self, message: MessageType, namespace: str) -> None:
        ...
