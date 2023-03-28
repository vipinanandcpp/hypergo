import copy
import importlib
import inspect
from typing import Any, Callable, List, Mapping, cast

import glom

from hypergo.config import Config
from hypergo.message import Message
from hypergo.types import TypeDict


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
        self._func_spec: Callable[..., Any] = Executor.func_spec(config.function)
        self._arg_spec: List[type] = Executor.arg_spec(self._func_spec)
        self._rettemplate: TypeDict = config.ret
        self._key: str = config.val
        self._args: List[str] = config.args

    def execute(self, message: Message) -> Message:
        # args: List[Any] = [argtype(glom.glom(message, arg)) for arg, argtype in zip(self._args, self._arg_spec)]
        args: List[Any] = []
        for arg, argtype in zip(self._args, self._arg_spec):
            if argtype == inspect.Parameter.empty:  # inspect._empty:
                args.append((glom.glom(message.to_dict(), arg)))
            else:
                args.append(argtype(glom.glom(message.to_dict(), arg)))
        ret: TypeDict = copy.deepcopy(self._rettemplate)
        glom.assign(ret, self._key, self._func_spec(*args))
        return Message({"body": ret, "routingkey": glom.glom(self._config, "pubtopic")})
