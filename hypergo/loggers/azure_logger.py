import logging
from typing import Optional, Union
from hypergo.loggers.base_logger import BaseLogger
from hypergo.loggers.datalink import DataLinkLogger, DataLinkTracer
from hypergo.metrics.datalink import DataLinkMetric
from hypergo.connectors.azure_application_insights import AzureApplicationInsights
from hypergo.secrets import Secrets


class AzureLogger(BaseLogger, AzureApplicationInsights):

    def __init__(self, secrets: Secrets, name: Optional[str] = None, log_level: int = logging.DEBUG,
                 log_format: Optional[Union[str, logging.Formatter]] = None):

        BaseLogger.__init__(self, name=name, log_level=log_level, log_format=log_format)
        AzureApplicationInsights.__init__(self, secrets=secrets)
        DataLinkLogger.set_log_exporter(log_exporter=self.log_exporter)
        DataLinkTracer.set_trace_exporter(trace_exporter=self.trace_exporter)
        DataLinkMetric.set_metric_exporter(self.metric_exporter)

    def get_handler(self):
        return DataLinkLogger.get_handler()

    def log(self, message: str, level: Optional[int] = None) -> None:
        if level is None:
            level = self.log_level
        handler: logging.Handler = self.get_handler()
        logger = logging.getLogger(self.name)
        logger.addHandler(handler)
        logger.setLevel(level)
        # Get a tracer for the current module.
        with DataLinkTracer.get_tracer(__name__).start_as_current_span(self.name, attributes={"trace-type": "user"}):
            # Log the message with the specified level
            logger.log(level, message)
