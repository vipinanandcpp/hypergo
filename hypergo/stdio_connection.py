from typing import Union

from hypergo.config import ConfigType
from hypergo.message import Message, MessageType
from hypergo.service_bus_connection import ServiceBusConnection
from hypergo.storage import Storage
import json


class StdioConnection(ServiceBusConnection):
    def __init__(self) -> None:
        pass

    def send(self, message: MessageType, namespace: str) -> None:
        print(json.dumps(message))
    
    def consume(self, stdio_message: str, config: ConfigType, storage: Union[Storage, None]) -> None:
        message: MessageType = Message.from_stdio_message(stdio_message)
        self.general_consume(message, config, storage)
