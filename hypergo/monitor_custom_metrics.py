import time
from functools import wraps
from typing import Any, Callable

from hypergo.monitors import DatalinkMonitor


def monitor_duration(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: Any, data: Any) -> Any:
        monitor = DatalinkMonitor(self.secrets, self.config["lib_func"])
        t0 = time.time()
        try:
            result = func(self, data)
        finally:
            t1 = time.time()
            monitor.send(metric_name="function_call_duration", metric_value=t1 - t0)
        return result

    return wrapper


def monitor_function_call_count(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: Any, data: Any) -> Any:
        monitor = DatalinkMonitor(self.secrets, self.config["lib_func"])
        try:
            result = func(self, data)
        finally:
            monitor.send(metric_name="function_call_count", metric_value=1)
        return result

    return wrapper
