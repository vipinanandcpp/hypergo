import time
from functools import wraps
from monitors import DatalinkMonitor


def monitor_duration(metadata):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor = DatalinkMonitor(metadata)
            t0 = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception:
                raise
            finally:
                t1 = time.time()
                monitor.send(metric_name="function_call_duration", metric_value=(t1-t0))
            return result
        return wrapper
    return decorator


def monitor_function_call_count(metadata):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor = DatalinkMonitor(metadata)
            try:
                result = func(*args, **kwargs)
            except Exception:
                raise
            finally:
                monitor.send(metric_name="function_call_count", metric_value=1)
            return result
        return wrapper
    return decorator