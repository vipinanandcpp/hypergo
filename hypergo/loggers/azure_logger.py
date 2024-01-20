import logging
from typing import Optional, Union
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import (LoggerProvider, LoggingHandler)
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

from hypergo.loggers.base_logger import BaseLogger
from hypergo.secrets import Secrets

trace.set_tracer_provider(TracerProvider())
# Attach LoggingHandler to root logger
logging.getLogger().addHandler(LoggingHandler())
logging.getLogger().setLevel(logging.NOTSET)


class AzureLogger(BaseLogger):
    exporter: AzureMonitorLogExporter = None
    logger_provider: LoggerProvider = LoggerProvider()
    set_logger_provider(logger_provider)

    def __init__(
        self,
        secrets: Secrets,
        name: Optional[str] = None,
        log_level: int = logging.DEBUG,
        log_format: Optional[Union[str, logging.Formatter]] = None,
    ) -> None:
        super().__init__(name=name, log_level=log_level, log_format=log_format)
        if not AzureLogger.exporter:
            AzureLogger.exporter = AzureMonitorLogExporter(
                connection_string=secrets.get("APPLICATIONINSIGHTS_CONNECTION_STRING"), disable_offline_storage=True)
            AzureLogger.logger_provider.add_log_record_processor(BatchLogRecordProcessor(AzureLogger.exporter))

    def log(self, message: str, level: Optional[int] = None) -> None:
        if level is None:
            level = self.log_level
        logger = logging.getLogger(self.name)
        logger.addHandler(self.get_handler())
        logger.setLevel(level)
        # Get a tracer for the current module.
        with trace.get_tracer(__name__).start_as_current_span(self.name):
            # Log the message with the specified level
            logger.log(level, message)
