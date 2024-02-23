import inspect
from functools import wraps
from typing import Any, Callable, Dict
from hypergo.metrics import custom_metrics_metadata
from hypergo.metrics.base_metrics import MetricResult
from hypergo.metrics.hypergo_metrics import HypergoMetric, Meter

__all__ = ["collect_metrics"]


def collect_metrics(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: Any, data: Any) -> Any:
        function_name: str = self.callback.__name__
        metric_callbacks: Dict[Callable[[MetricResult], MetricResult], MetricResult] = {}
        for custom_metrics in custom_metrics_metadata:
            for metric_callback in HypergoMetric.get_metrics_callback(package=custom_metrics.package,
                                                                      module_name=custom_metrics.module_name,
                                                                      class_name=custom_metrics.class_name):
                metric_callbacks.setdefault(metric_callback, metric_callback())
        # if func is an instance method of self then func(data) is called. Else it's a decorated function
        result: Any = func(data) if inspect.ismethod(func) and self == func.__self__ else func(self, data)
        meter: Meter = HypergoMetric.get_meter(name=function_name)
        for metric_callback, value in metric_callbacks.items():
            HypergoMetric.send(meter=meter, metric_name=metric_callback.__name__, metric_result=metric_callback(value),
                               description=metric_callback.__doc__)
        return result
    return wrapper
