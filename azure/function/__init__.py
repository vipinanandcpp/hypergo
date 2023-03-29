import azure.functions as func
import os
from hypergo.config import Config
from hypergo.azure_service_bus_connection import AzureServiceBusConnection
from hypergo.service_bus_connection import ServiceBusConnection


def main(message: func.ServiceBusMessage) -> None:
    conn_str: str = os.getenv("SERVICE_BUS_CONNECTION_STRING")
    connection: ServiceBusConnection = AzureServiceBusConnection(conn_str)
    connection.consume(message, Config.from_yaml("./config.yaml"))

