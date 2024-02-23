from logging import Handler
from typing import Type
from opentelemetry._logs import set_logger_provider, get_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import LogExporter, BatchLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SpanExporter, BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider, get_tracer_provider, get_tracer

LogExporter = Type[LogExporter]
TraceExporter = Type[SpanExporter]


class HypergoLogger:
    is_logger_provider_set: bool = False

    @staticmethod
    def set_log_exporter(log_exporter: LogExporter):
        if not HypergoLogger.is_logger_provider_set:
            set_logger_provider(LoggerProvider())
            HypergoLogger.is_logger_provider_set = True
        get_logger_provider().add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    @staticmethod
    def get_handler() -> Handler:
        return LoggingHandler(logger_provider=get_logger_provider())


class HypergoTracer:
    is_tracer_provider_set: bool = False

    @staticmethod
    def set_trace_exporter(trace_exporter: TraceExporter):
        if not HypergoTracer.is_tracer_provider_set:
            set_tracer_provider(TracerProvider())
            HypergoTracer.is_tracer_provider_set = True
        get_tracer_provider().add_span_processor(BatchSpanProcessor(span_exporter=trace_exporter))

    @staticmethod
    def get_tracer(name: str):
        return get_tracer(name)
