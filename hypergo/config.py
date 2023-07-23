import json
from typing import Any, Dict, List

import yaml
from typing_extensions import NotRequired

from hypergo.custom_types import TypedDictType


class ConfigType(TypedDictType):
    namespace: str
    name: str
    package: str
    lib_func: str
    input_keys: List[str]
    output_keys: List[str]
    input_bindings: List[str]
    output_bindings: List[str]
    input_operations: NotRequired[List[str]]
    output_operations: NotRequired[List[str]]
    custom_properties: NotRequired[Dict[str, Any]]


class Config:
    @staticmethod
    def from_yaml(file_name: str) -> ConfigType:
        with open(file_name, "r", encoding="utf-8") as file_handle:
            cfg_dict: ConfigType = yaml.safe_load(file_handle)
            return cfg_dict

    @staticmethod
    def from_json(file_name: str) -> ConfigType:
        with open(file_name, "r", encoding="utf-8") as file_handle:
            cfg_dict: ConfigType = json.load(file_handle)
            return cfg_dict
