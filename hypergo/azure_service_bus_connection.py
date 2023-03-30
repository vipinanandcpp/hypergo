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
        # self._service_bus_client: ServiceBusClient = ServiceBusClient.from_connection_string(conn_str)

    def send(self, message: Message, topic: str) -> None:
        asbm: ServiceBusMessage = message.to_azure_service_bus_service_bus_message()
        with self._service_bus_client:
            sender: ServiceBusSender = self._service_bus_client.get_topic_sender(topic)
            sender.send_messages(asbm)

    def consume(self, msg: func.ServiceBusMessage, config: Config) -> None:
        message: Message = Message.from_azure_functions_service_bus_message(msg)
        executor: Executor = AzureServiceBusExecutor(config)
        self.send(executor.execute(message), config.namespace)

    def execute(self, msg: func.ServiceBusMessage, config: Config) -> func.Out[str]:
        message: Message = Message.from_azure_functions_service_bus_message(msg)
        executor: Executor = AzureServiceBusExecutor(config)
        return executor.execute(message).to_azure_service_bus_service_bus_message()
