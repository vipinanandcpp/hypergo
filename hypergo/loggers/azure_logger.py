import logging
from typing import Optional, Union
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from hypergo.loggers.base_logger import BaseLogger
from hypergo.secrets import Secrets


# Ensure that configure_azure_monitor is called only once
configure_azure_monitor_called: bool = False


class AzureLogger(BaseLogger):
    def __init__(
        self,
        secrets: Secrets,
        name: Optional[str] = None,
        log_level: int = logging.DEBUG,
        log_format: Optional[Union[str, logging.Formatter]] = None,
    ) -> None:
        super().__init__(name=name, log_level=log_level, log_format=log_format)
        global configure_azure_monitor_called
        if not configure_azure_monitor_called:
            configure_azure_monitor(connection_string=secrets.get("APPLICATIONINSIGHTS-CONNECTION-STRING"),
                                    disable_offline_storage=True)
            configure_azure_monitor_called = True

    def log(self, message: str, level: Optional[int] = None) -> None:
        if level is None:
            level = self.log_level
        handler: logging.Handler = self.get_handler()
        logger = logging.getLogger(self.name)
        logger.addHandler(handler)
        logger.setLevel(level)
        # Get a tracer for the current module.
        with trace.get_tracer(__name__).start_as_current_span(self.name):
            # Log the message with the specified level
            logger.log(level, message)
