import azure.functions as func
from azure.servicebus import (ServiceBusClient, ServiceBusMessage,
                              ServiceBusSender)

from hypergo.azure_service_bus_executor import AzureServiceBusExecutor
from hypergo.config import Config
from hypergo.executor import Executor
from hypergo.message import Message
from hypergo.service_bus_connection import ServiceBusConnection


class AzureServiceBusConnection(ServiceBusConnection):
    def __init__(self, conn_str: str) -> None:
        self._service_bus_client: ServiceBusClient = ServiceBusClient.from_connection_string(conn_str)

    def send(self, message: Message) -> None:
        asbm: ServiceBusMessage = message.to_azure_service_bus_service_bus_message()
        with self._service_bus_client:
            sender: ServiceBusSender = self._service_bus_client.get_topic_sender("datalink")
            sender.send_messages(asbm)
            print("sent : " + str(asbm))

    def consume(self, message: func.ServiceBusMessage, cfg: Config) -> None:
        msg: Message = Message.from_azure_functions_service_bus_message(message)
        executor: Executor = AzureServiceBusExecutor(cfg)
        self.send(executor.execute(msg))
