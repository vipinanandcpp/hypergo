from abc import ABC, abstractmethod
from typing import Optional, Union


class MetricResult:
    __slots__ = ("unit", "value", "name")

    def __init__(self, unit: str, value: Union[float, int], name: Optional[str] = None) -> None:
        self.unit: str = unit
        self.value: Union[float, int] = value
        self.name = name


class ExecutionTimeMetrics(ABC):
    @staticmethod
    @abstractmethod
    def function_total_execution_time(popped_result: MetricResult = None) -> MetricResult:
        pass


class ResourceUsageMetrics(ABC):
    @staticmethod
    @abstractmethod
    def cpu_usage(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def memory_usage(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def disk_io_bytes(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def disk_io_time(popped_result: MetricResult = None) -> MetricResult:
        pass


class ThroughputMetrics(ABC):
    @staticmethod
    @abstractmethod
    def requests_per_second(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def concurrency(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def queue_length(popped_result: MetricResult = None) -> MetricResult:
        pass


class ErrorMetrics(ABC):
    @staticmethod
    @abstractmethod
    def error_rate(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def error_types(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def error_messages(popped_result: MetricResult = None) -> MetricResult:
        pass


class LatencyMetrics(ABC):
    @staticmethod
    @abstractmethod
    def function_start_latency(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def end_to_end_latency(popped_result: MetricResult = None) -> MetricResult:
        pass


class DependencyMetrics(ABC):
    @staticmethod
    @abstractmethod
    def external_service_calls(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def dependency_health(popped_result: MetricResult = None) -> MetricResult:
        pass


class ResourceUtilizationMetrics(ABC):
    @staticmethod
    @abstractmethod
    def database_queries(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def cache_hits_and_misses(popped_result: MetricResult = None) -> MetricResult:
        pass


class ConcurrencyMetrics(ABC):
    @staticmethod
    @abstractmethod
    def concurrent_executions(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def queue_wait_time(popped_result: MetricResult = None) -> MetricResult:
        pass


class CostMetrics(ABC):
    @staticmethod
    @abstractmethod
    def resource_costs(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def resource_utilization_vs_cost(popped_result: MetricResult = None) -> MetricResult:
        pass


class SecurityMetrics(ABC):
    @staticmethod
    @abstractmethod
    def authentication_attempts(popped_result: MetricResult = None) -> MetricResult:
        pass

    @staticmethod
    @abstractmethod
    def security_alerts(popped_result: MetricResult = None) -> MetricResult:
        pass
