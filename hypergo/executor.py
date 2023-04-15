import importlib
import inspect
from typing import Any, Callable, List, Mapping, cast, get_origin

import glom

from hypergo.config import Config
from hypergo.custom_types import TypeDict
from hypergo.message import Message


class Executor:
    @staticmethod
    def func_spec(fn_name: str) -> Callable[..., Any]:
        tokens: List[str] = fn_name.split(".")
        return cast(Callable[..., Any], (getattr(importlib.import_module(".".join(tokens[:-1])), tokens[-1])))

    @staticmethod
    def arg_spec(func: Callable[..., Any]) -> List[type]:
        params: Mapping[str, inspect.Parameter] = inspect.signature(func).parameters
        return [params[k].annotation for k in list(params.keys())]

    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._func_spec: Callable[..., Any] = Executor.func_spec(config.lib_func)
        self._arg_spec: List[type] = Executor.arg_spec(self._func_spec)

    def execute(self, message: Message) -> Message:
        # args: List[Any] = [argtype(glom.glom(message, arg)) for arg, argtype in zip(self._args, self._arg_spec)]
        args: List[Any] = []

        def safecast(typingtype):
            return {inspect.Parameter.empty: lambda identity: identity}.get(typingtype, get_origin(typingtype)) or typingtype

        for arg, argtype in zip(self._config.input_bindings, self._arg_spec):
            if argtype == inspect.Parameter.empty:  # inspect._empty:
                args.append((glom.glom(message.to_dict(), arg)))
            else:
                args.append(safecast(argtype)(glom.glom(message.to_dict(), arg)))

        execution: Any = self._func_spec(*args)
        results = list(execution) if inspect.isgenerator(execution) else [execution]

        for result in results:
            msg: TypeDict = {"routingkey": self.clean_routing_keys(self._config.output_keys), "body": {}}

            def handle_tuple(dst, src):
                for binding, tuple_elem in zip(self._config.output_bindings, src):
                    glom.assign(dst, binding, tuple_elem, missing=dict)

            def handle_default(dst, src):
                for binding in self._config.output_bindings:
                    glom.assign(dst, binding, src, missing=dict)
           
            def handle_list(dst, src):
                for binding in self._config.output_bindings:
                    glom.assign(dst, binding, src[:3], missing=dict)

            {
                tuple: handle_tuple,
                list: handle_list
            }.get(type(result), handle_default)(msg, result)

            yield Message(msg)

    def clean_routing_keys(self, keys: List[str]) -> str:
        return ".".join(sorted(set(".".join(keys).split("."))))
