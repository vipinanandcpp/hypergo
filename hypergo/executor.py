import importlib
import inspect
from typing import Any, Callable, List, Mapping, cast

import glom

from hypergo.config import Config
from hypergo.message import Message
from hypergo.custom_types import TypeDict


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

        for arg, argtype in zip(self._config.input_bindings, self._arg_spec):
            if argtype == inspect.Parameter.empty:  # inspect._empty:
                args.append((glom.glom(message.to_dict(), arg)))
            else:
                args.append(argtype(glom.glom(message.to_dict(), arg)))
        
        execution: Any = self._func_spec(*args)
        results: dict[type, Any] = { 
            type(iter(())): list(execution)
        }.get(execution, [execution])
        
        for result in results:            
            msg: TypeDict = {
                "routingkey": self.clean_routing_keys(self._config.output_keys),
                "body": {}
            }
            def handle_tuple(m, r):
                for binding, tuple_elem in zip(self._config.output_bindings, r):
                    glom.assign(m, binding, tuple_elem, missing=dict)

            def handle_default(m, r):
                for binding in self._config.output_bindings:
                    glom.assign(m, binding, r, missing=dict)
            {
                tuple: handle_tuple(msg, result)
            }.get(result, handle_default(msg, result))
            
            yield Message(msg)

    def clean_routing_keys(self, keys: List[str]) -> str:
        return ".".join(sorted(set(".".join(keys).split("."))))
