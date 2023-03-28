import json

import azure.functions as func
from azure.servicebus import ServiceBusMessage

from hypergo.types import TypeDict


class Message:
    @staticmethod
    def from_azure_functions_service_bus_message(message: func.ServiceBusMessage) -> 'Message':
        return Message({"body": json.loads(message.get_body().decode('utf-8')), "routingkey": message.user_properties["routingkey"]})

    def to_azure_service_bus_service_bus_message(self) -> ServiceBusMessage:
        print("routingkey: " + self._routingkey)
        ret: ServiceBusMessage = ServiceBusMessage(body=json.dumps(self._body), application_properties={"routingkey": self._routingkey})
        return ret

    def __init__(self, struct: TypeDict) -> None:
        self._body: TypeDict = struct["body"]
        self._routingkey: str = struct["routingkey"]

    def to_dict(self) -> TypeDict:
        return {"body": self._body, "routingkey": self._routingkey}

    @property
    def body(self) -> TypeDict:
        return self._body

    @property
    def routingkey(self) -> str:
        return self._routingkey
