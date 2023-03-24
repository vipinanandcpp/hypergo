from abc import ABC, abstractmethod
from typing import Any, Dict, Union

import azure.functions as func
import yaml

from hypergo.executor import Executor


class Message(ABC):
    @staticmethod
    def create(message: Any) -> 'Message':
        from hypergo.azure_service_bus_message import AzureServiceBusMessage  # pylint: disable=import-outside-toplevel, cyclic-import
        from hypergo.dict_message import DictMessage  # pylint: disable=import-outside-toplevel, cyclic-import

        return {dict: DictMessage, func.ServiceBusMessage: AzureServiceBusMessage}[type(message)](message)

    def __init__(self, message: Union['AzureServiceBusMessage', 'DictMessage']) -> None:  # noqa: F821
        from hypergo.azure_service_bus_message import AzureServiceBusMessage  # pylint: disable=import-outside-toplevel, cyclic-import
        from hypergo.dict_message import DictMessage  # pylint: disable=import-outside-toplevel, cyclic-import

        self._message: Union[AzureServiceBusMessage, DictMessage] = message

    @abstractmethod
    def get_meta(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_rk(self) -> str:
        ...

    def consume(self) -> Dict[str, Any]:
        with open("./config.yaml", "r", encoding="utf-8") as file_handle:
            config: Dict[str, Any] = yaml.safe_load(file_handle)
            payload = {"data": self.get_data(), "meta": {"routingkey": self.get_rk()}}
            print(payload)
            return {"meta": {"routingkey": "x.y.z"}, "content": Executor(config).execute(payload)}

    @abstractmethod
    def send(self, message: Dict[str, Any]) -> None:
        ...
