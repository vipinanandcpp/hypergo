import copy
import importlib
import inspect
from typing import Any, Callable, Dict, List, Mapping, Type, cast
import glom


class Executor:
    @staticmethod
    def func_spec(fn_name: str) -> Callable[..., Any]:
        tokens: List[str] = fn_name.split(".")
        return cast(Callable[..., Any], (getattr(importlib.import_module(".".join(tokens[:-1])), tokens[-1])))

    @staticmethod
    def arg_spec(func: Callable[..., Any]) -> List[Type]:
        params: Mapping[str, inspect.Parameter] = inspect.signature(func).parameters
        return [params[k].annotation for k in list(params.keys())]

    def __init__(self, config: Dict[str, Any]) -> None:
        self._func_spec: Callable = Executor.func_spec(config["function"])
        self._arg_spec: List[Type] = Executor.arg_spec(self._func_spec)
        self._rettemplate: Dict[str, Any] = config["ret"]
        self._key: str = config["val"]
        self._args: List[str] = config["args"]

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        args: List[Any] = [argtype(glom.glom(context, arg)) for arg, argtype in zip(self._args, self._arg_spec)]
        ret: Dict[str, Any] = copy.deepcopy(self._rettemplate)
        glom.assign(ret, self._key, str(self._func_spec(*args)))
        return ret
