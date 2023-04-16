import importlib
import inspect
from typing import (Any, Callable, Dict, Generator, List, Mapping, cast,
                    get_origin)

import glom
import logging
from hypergo.config import Config
from hypergo.custom_types import TypeDict
from hypergo.message import Message


class Executor:
    @staticmethod
    def func_spec(fn_name: str) -> Callable[..., Any]:
        tokens: List[str] = fn_name.split(".")
        logger = logging.getLogger(__name__)
        logger.warn((f'Tokens: {tokens}'))
        return cast(Callable[..., Any], (getattr(importlib.import_module(".".join(tokens[:-1])), tokens[-1])))

    @staticmethod
    def arg_spec(func: Callable[..., Any]) -> List[type]:
        params: Mapping[str, inspect.Parameter] = inspect.signature(func).parameters
        return [params[k].annotation for k in list(params.keys())]

    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._func_spec: Callable[..., Any] = Executor.func_spec(config.lib_func)
        self._arg_spec: List[type] = Executor.arg_spec(self._func_spec)

    def get_args(self, message: Dict[str, Any]) -> List[Any]:
        # args: List[Any] = [argtype(glom.glom(message, arg)) for arg, argtype in zip(self._args, self._arg_spec)]
        args: List[Any] = []

        # T = TypeVar('T')

        def safecast(some_type: type) -> Callable[..., Any]:
            if some_type == inspect.Parameter.empty:
                return lambda value: value
            return get_origin(some_type) or some_type

        for arg, argtype in zip(self._config.input_bindings, self._arg_spec):
            if argtype == inspect.Parameter.empty:  # inspect._empty:
                args.append((glom.glom(message, arg)))
            else:
                args.append(safecast(argtype)(glom.glom(message, arg)))

        return args

    def execute(self, message: Message) -> Generator[Message, None, None]:
        args: List[Any] = self.get_args(message.to_dict())
        execution: Any = self._func_spec(*args)
        results: List[Any] = list(execution) if inspect.isgenerator(execution) else [execution]

        for result in results:
            msg: TypeDict = {"routingkey": self.clean_routing_keys(self._config.output_keys), "body": {}}

            def handle_tuple(dst: TypeDict, src: Any) -> None:
                for binding, tuple_elem in zip(self._config.output_bindings, src):
                    glom.assign(dst, binding, tuple_elem, missing=dict)

            def handle_default(dst: TypeDict, src: Any) -> None:
                for binding in self._config.output_bindings:
                    glom.assign(dst, binding, src, missing=dict)

            def handle_list(dst: TypeDict, src: Any) -> None:
                for binding in self._config.output_bindings:
                    # src[:3] is a debugging hack !!REMOVE!!!
                    glom.assign(dst, binding, src[:3], missing=dict)

            if isinstance(result, tuple):
                handle_tuple(msg, result)
            elif isinstance(result, list):
                handle_list(msg, result)
            else:
                handle_default(msg, result)
            # {tuple: handle_tuple, list: handle_list}.get(type(result), handle_default)(msg, result)

            yield Message(msg)

    def clean_routing_keys(self, keys: List[str]) -> str:
        return ".".join(sorted(set(".".join(keys).split("."))))
