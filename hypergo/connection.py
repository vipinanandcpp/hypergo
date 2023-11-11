from abc import ABC, abstractmethod
from typing import cast, Optional

from hypergo.config import ConfigType
from hypergo.executor import Executor
from hypergo.message import MessageType
from hypergo.loggers.base_logger import BaseLogger as Logger
from hypergo.secrets import Secrets
from hypergo.storage import Storage


class Connection(ABC):
    def general_consume(
        self,
        message: MessageType,
        config: ConfigType,
        storage: Optional[Storage] = None,
        secrets: Optional[Secrets] = None,
        logger:  Optional[Logger] = None
    ) -> None:
        executor: Executor = Executor(config, storage, secrets, logger)
        for execution in executor.execute(message):
            self.send(cast(MessageType, execution), config["namespace"])

    @abstractmethod
    def send(self, message: MessageType, namespace: str) -> None:
        ...
