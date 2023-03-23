from abc import ABC, abstractmethod
import yaml
from typing import Any, Dict, Union
import azure.functions as func
from executor import Executor

class Message(ABC):
    @staticmethod
    def create(message: Any) -> 'Message':
        from dict_message import DictMessage
        from azure_service_bus_message import AzureServiceBusMessage
        return {
            dict: DictMessage,
            func.ServiceBusMessage: AzureServiceBusMessage
        }[type(message)](message)

    def __init__(self, message: 'Union[AzureServiceBusMessage, DictMessage]') -> None:
        from dict_message import DictMessage
        from azure_service_bus_message import AzureServiceBusMessage
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
        with open("./config.yaml", "r") as f:
            config: Dict[str, Any] = yaml.safe_load(f)
            payload = {
                    "data": self.get_data(),
                    "meta": {
                        "routingkey": self.get_rk()
                    }
                }
            print(payload)
            return {
                "meta": {
                    "routingkey": "x.y.z"
                },
                "content": Executor(config).execute(payload)
            }

    @abstractmethod
    def send(self, message: Dict[str, Any]) -> None:
        ...

