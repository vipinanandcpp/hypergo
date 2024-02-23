from azure.monitor.opentelemetry.exporter import (AzureMonitorLogExporter, AzureMonitorTraceExporter,
                                                  AzureMonitorMetricExporter)
from hypergo.loggers.hypergo_logger import LogExporter, TraceExporter
from hypergo.metrics.hypergo_metrics import MetricExporter
from hypergo.secrets import Secrets


class AzureApplicationInsights:
    def __init__(self, secrets: Secrets):
        self._log_exporter: LogExporter = AzureMonitorLogExporter(connection_string=
                                                                 secrets.get("APPLICATIONINSIGHTS-CONNECTION-STRING"))
        self._trace_exporter: TraceExporter = AzureMonitorTraceExporter(connection_string=
                                                                     secrets.get("APPLICATIONINSIGHTS-CONNECTION-STRING"
                                                                                 ))
        self._metric_exporter: MetricExporter = AzureMonitorMetricExporter(connection_string=
                                                                     secrets.get("APPLICATIONINSIGHTS-CONNECTION-STRING"
                                                                                 ))

    @property
    def log_exporter(self):
        return self._log_exporter

    @property
    def trace_exporter(self):
        return self._trace_exporter

    @property
    def metric_exporter(self):
        return self._metric_exporter
