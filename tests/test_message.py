import json
import unittest
from typing import Any, Dict, Mapping, Union
from unittest.mock import MagicMock

import azure.functions as func

from hypergo.message import Message


class TestMessage(unittest.TestCase):
    def test_from_http_request_bad_json(self) -> None:
        with self.assertRaises(json.JSONDecodeError):
            http_request = func.HttpRequest(
                method='POST',
                body="bad json".encode('utf-8'),
                url='/api/HttpTrigger/other_tag',
                params=None)

            Message.from_http_request(http_request)

    def test_from_http_request_happy_path(self) -> None:
        http_request = func.HttpRequest(
                method='POST',
                body='{"good": "json"}'.encode('utf-8'),
                url='/api/HttpTrigger/other_tag',
                params=None)
        result = Message.from_http_request(http_request)

        self.assertEquals(result['body'],  {'good': 'json'})
        self.assertEquals(result['routingkey'], 'http_request.api.HttpTrigger.other_tag')

if __name__ == '__main__':
    # Run the unit tests
    unittest.main()