from typing import List, cast

import yaml

from hypergo.types import TypeDict


class Config:
    @staticmethod
    def from_yaml(file_name: str) -> 'Config':
        with open(file_name, "r", encoding="utf-8") as file_handle:
            cfg_dict: TypeDict = yaml.safe_load(file_handle)
            return Config.from_dict(cfg_dict)

    @staticmethod
    def from_dict(cfg_dict: TypeDict) -> 'Config':
        return Config(cfg_dict)

    def __init__(self, cfg_dict: TypeDict) -> None:
        self._namespace: str = cast(str, cfg_dict.get("namespace"))
        self._function: str = cast(str, cfg_dict.get("function"))
        self._subtopic: str = cast(str, cfg_dict.get("subtopic"))
        self._pubtopic: str = cast(str, cfg_dict.get("pubtopic"))
        self._args: List[str] = cast(List[str], cfg_dict.get("args"))
        self._val: str = cast(str, cfg_dict.get("val"))
        self._ret: TypeDict = cast(TypeDict, cfg_dict.get("ret"))

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def function(self) -> str:
        return self._function

    @property
    def subtopic(self) -> str:
        return self._subtopic

    @property
    def pubtopic(self) -> str:
        return self._pubtopic

    @property
    def args(self) -> List[str]:
        return self._args

    @property
    def val(self) -> str:
        return self._val

    @property
    def ret(self) -> TypeDict:
        return self._ret
