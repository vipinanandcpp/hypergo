import os
import sys
import logging
from uuid import uuid4
import unittest
from unittest.mock import Mock, patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from hypergo.loggers.azure_logger import AzureLogger


class TestAzureLogger(unittest.TestCase):

    @patch.dict(os.environ, {"APPLICATIONINSIGHTS-CONNECTION-STRING": f"InstrumentationKey={uuid4()};IngestionEndpoint=https://eastus2-3.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus2.livediagnostics.monitor.azure.com/"})
    @patch("hypergo.loggers.azure_logger.configure_azure_monitor")
    @patch("opentelemetry.trace.get_tracer")
    @patch("hypergo.secrets.LocalSecrets")
    def test_azure_logger(self, MockSecrets, mock_get_tracer, mock_configure_azure_monitor):
        # Create a mock instance for secrets
        mock_secrets_instance = Mock()
        mock_secrets_instance.get.return_value = os.environ["APPLICATIONINSIGHTS-CONNECTION-STRING"]
        MockSecrets.return_value = mock_secrets_instance

        mock_get_tracer.return_value.__enter__ = Mock()
        mock_get_tracer.return_value.__exit__ = Mock()

        # Create an instance of AzureLogger
        logger = AzureLogger(secrets=MockSecrets.return_value)

        mock_configure_azure_monitor.assert_called_with(connection_string=mock_secrets_instance.get.return_value,
                                                        disable_offline_storage=True
                                                        )

        logger.log("Test message", level=logging.INFO)
        mock_get_tracer.assert_called_with('hypergo.loggers.azure_logger')


if __name__ == '__main__':
    unittest.main()
