from logging import Handler
from typing import cast
from opentelemetry._logs import set_logger_provider, get_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import LogExporter, BatchLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SpanExporter as TraceExporter, BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider, get_tracer_provider, get_tracer, Tracer


class HypergoLogger:
    is_logger_provider_set: bool = False

    @staticmethod
    def set_log_exporter(log_exporter: LogExporter) -> None:
        if not HypergoLogger.is_logger_provider_set:
            set_logger_provider(LoggerProvider())
            HypergoLogger.is_logger_provider_set = True
        cast(LoggerProvider, get_logger_provider()).add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    @staticmethod
    def get_handler() -> Handler:
        return LoggingHandler(logger_provider=get_logger_provider())


class HypergoTracer:
    is_tracer_provider_set: bool = False

    @staticmethod
    def set_trace_exporter(trace_exporter: TraceExporter) -> None:
        if not HypergoTracer.is_tracer_provider_set:
            set_tracer_provider(TracerProvider())
            HypergoTracer.is_tracer_provider_set = True
        cast(TracerProvider, get_tracer_provider()).add_span_processor(BatchSpanProcessor(span_exporter=trace_exporter))

    @staticmethod
    def get_tracer(name: str) -> Tracer:
        return get_tracer(name)
