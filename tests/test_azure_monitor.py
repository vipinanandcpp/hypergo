import os
import sys
import unittest
from uuid import uuid4
from unittest.mock import Mock, patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from hypergo.message import MessageType
from hypergo.config import ConfigType
from hypergo.executor import Executor
from hypergo.loggers.azure_logger import AzureLogger


class TestAzureMonitor(unittest.TestCase):
    def setUp(self) -> None:
        self.message: MessageType = {
            "body": [{"name": "Chris", "company": "LinkLogistics"}],
            "routingkey": "a.b.c.x"
        }
        return super().setUp()

    @patch.dict(os.environ, {"APPLICATIONINSIGHTS-CONNECTION-STRING": f"InstrumentationKey={uuid4()};IngestionEndpoint=https://eastus2-3.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus2.livediagnostics.monitor.azure.com/"})
    @patch("hypergo.metrics.hypergo_metrics.HypergoMetric.send")
    @patch("hypergo.metrics.hypergo_metrics.HypergoMetric.get_meter")
    @patch("hypergo.loggers.hypergo_logger.HypergoTracer.get_tracer")
    @patch("hypergo.secrets.LocalSecrets")
    def test_azure_monitor(self, mock_secrets, mock_get_tracer, mock_get_meter, mock_send):
        cfg: ConfigType = {
                            "version": "2.0.0",
                            "namespace": "testing",
                            "name": "batchstreamer",
                            "package": "ldp-batch-to-stream-producer",
                            "lib_func": "batch_to_stream_producer.__main__.batch_to_stream",
                            "input_keys": ["a.b.c", "a.b.d", "a.b", "a"],
                            "output_keys": ["y.h.?.?"],
                            "input_bindings": ["{message.body}", None],
                            "output_bindings": ["message.body"]
                        }
        mock_secrets.get.return_value = os.environ["APPLICATIONINSIGHTS-CONNECTION-STRING"]
        mock_get_tracer.return_value.__enter__ = Mock()
        mock_get_tracer.return_value.__exit__ = Mock()

        # Create an instance of AzureLogger
        logger = AzureLogger(secrets=mock_secrets)
        executor = Executor(cfg, logger=logger)
        for _ in executor.execute(self.message):
            pass
        mock_get_meter.assert_called_with(name="batch_to_stream")
        assert mock_send.call_count == 5


if __name__ == '__main__':
    unittest.main()
