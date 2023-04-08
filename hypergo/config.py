from typing import List, cast

import yaml
import json

from hypergo.custom_types import TypeDict


class Config:
    @staticmethod
    def from_yaml(file_name: str) -> 'Config':
        with open(file_name, "r", encoding="utf-8") as file_handle:
            cfg_dict: TypeDict = yaml.safe_load(file_handle)
            return Config.from_dict(cfg_dict)

    @staticmethod
    def from_json(file_name: str) -> 'Config':
        with open(file_name, "r", encoding="utf-8") as file_handle:
            cfg_dict: TypeDict = json.load(file_handle)
            return Config.from_dict(cfg_dict)


    @staticmethod
    def from_dict(cfg_dict: TypeDict) -> 'Config':
        return Config(cfg_dict)

    def __init__(self, cfg_dict: TypeDict) -> None:
        self._namespace: str = cast(str, cfg_dict.get("namespace"))
        self._lib_func: str = cast(str, cfg_dict.get("lib_func"))
        self._input_keys: List[str] = cast(List[str], cfg_dict.get("input_keys"))
        self._output_keys: List[str] = cast(List[str], cfg_dict.get("output_keys"))
        self._input_bindings: List[str] = cast(List[str], cfg_dict.get("input_bindings"))
        self._output_bindings: List[str] = cast(List[str], cfg_dict.get("output_bindings"))

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def lib_func(self) -> str:
        return self._lib_func

    @property
    def input_keys(self) -> List[str]:
        return self._input_keys

    @property
    def output_keys(self) -> List[str]:
        return self._output_keys

    @property
    def input_bindings(self) -> List[str]:
        return self._input_bindings

    @property
    def output_bindings(self) -> List[str]:
        return self._output_bindings
