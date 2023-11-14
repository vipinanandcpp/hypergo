import glom
import os
import sys
import unittest
from unittest.mock import patch
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from hypergo.message import MessageType
from hypergo.config import ConfigType
from hypergo.context import ContextType
from hypergo.executor import Executor


class TestDynamicRoutingKey(unittest.TestCase):
    def setUp(self) -> None:
        self.message: MessageType = {
            "body": {},
            "routingkey": "link.db.query.specleasing.scheduled.select_query"
        }
        return super().setUp()

    @patch("hypergo.monitors.requests.post")
    @patch.dict(os.environ, {"LOG_ANALYTICS_WORKSPACE_ID": "shmorkspace_id"})
    @patch.dict(os.environ, {"LOG_ANALYTICS_PRIMARY_KEY": "shmimary_key"})
    def test_dynamic_routing_key(self, mock_post):
        cfg: ConfigType = {
                            "namespace": "datalink",
                            "name": "snowflakedbexecutor",
                            "package": "ldp-db-executor",
                            "lib_func": "dbexecutor.snowflake_db_executor.__main__.execute",
                            "input_keys": ["link.db.query"],
                            "output_keys": ["?.db.result.link.json"],
                            "input_bindings": ["{config.custom_properties.?}"],
                            "output_bindings": ["message.body.snowflake.db.record"],
                            "custom_properties": {"specleasing.select_query":
                                            "SELECT * FROM DP_LNK_DEV_DB.DP_LNK_ENTITIES.VW_UNIT_VALUATIONS LIMIT 10;"}
                        }
        response = requests.Response()
        response.status_code = 200
        mock_post.return_value = response
        executor = Executor(cfg)
        context: ContextType = {"message": self.message, "config": cfg}
        try:
            executor.get_args(context=context)
        except glom.PathAccessError as e:
            raise e

if __name__ == '__main__':
    unittest.main()