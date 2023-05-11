import json
from typing import Any, Dict, Optional
from unittest import TestCase, mock

import azure.functions as func
from azure.servicebus import ServiceBusMessage
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hypergo.message import MessageType, Message

class TestMessage(TestCase):
    def setUp(self) -> None:
        self.example_message: MessageType = {
            "body": {"key": "value"},
            "routingkey": "example.routing.key",
            "storagekey": "example.storage.key",
        }
        self.example_service_bus_message: ServiceBusMessage = ServiceBusMessage(
            body=json.dumps(self.example_message["body"]).encode("utf-8"),
            user_properties={"routingkey": self.example_message["routingkey"]},
        )

    # def test_from_azure_functions_service_bus_message(self) -> None:
    #     message: MessageType = Message.from_azure_functions_service_bus_message(self.example_service_bus_message)
    #     expected_message: MessageType = MessageType(**self.example_message)
    #     self.assertEqual(message, expected_message)

    def test_to_azure_service_bus_service_bus_message(self) -> None:
        message: MessageType = MessageType(**self.example_message)
        expected_service_bus_message: ServiceBusMessage = ServiceBusMessage(
            body=json.dumps(message["body"]).encode("utf-8"),
            application_properties={"routingkey": message["routingkey"]},
        )
        service_bus_message: ServiceBusMessage = Message.to_azure_service_bus_service_bus_message(message)
        self.assertEqual(service_bus_message.body, expected_service_bus_message.body)
        self.assertEqual(service_bus_message.application_properties, expected_service_bus_message.application_properties)
