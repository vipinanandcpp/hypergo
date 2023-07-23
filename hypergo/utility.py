import base64
import hashlib
import inspect
import json
import types
from typing import Any, Dict, Mapping, Union, cast, get_origin, List

import dill
import glom
import pydash
import yaml

from hypergo.custom_types import JsonDict, JsonType, TypedDictType

def traverse_datastructures(func):
    def wrapper(value):
        return {
            dict: lambda d: {wrapper(k): wrapper(v) for k, v in d.items()},
            list: lambda l: [wrapper(i) for i in l]
        }.get(type(value), func)(value)

    return wrapper


class Utility:
    @staticmethod
    def deep_get(dic: Union[TypedDictType, Dict[str, Any]], key: str) -> Any:
        result = pydash.get(dic, key)
        if not result:
            raise KeyError(f"Spec {key}  not found in the dictionary")
        return result

    @staticmethod
    def deep_set(dic: Union[TypedDictType, Dict[str, Any]], key: str, val: Any) -> None:
        glom.assign(dic, key, val, missing=dict)

    @staticmethod
    def yaml_read(file_name: str) -> Mapping[str, Any]:
        with open(file_name, "r", encoding="utf-8") as file_handle:
            return cast(Mapping[str, Any], yaml.safe_load(file_handle))

    @staticmethod
    def yaml_write(file_name: str, dic: Union[TypedDictType, Dict[str, Any]]) -> None:
        pass

    @staticmethod
    def json_read(file_name: str) -> Mapping[str, Any]:
        with open(file_name, "r", encoding="utf-8") as file_handle:
            return cast(Mapping[str, Any], json.load(file_handle))

    @staticmethod
    def json_write(file_name: str, dic: Dict[str, Any]) -> None:
        pass

    @staticmethod
    def hash(content: str) -> str:
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    @staticmethod
    def safecast(expected_type: type, provided_value: Any) -> Any:
        ret: Any = provided_value
        value_type: Any = get_origin(expected_type) or expected_type

        if value_type not in [
            int,
            float,
            complex,
            bool,
            str,
            bytes,
            bytearray,
            memoryview,
            list,
            tuple,
            range,
            set,
            frozenset,
            dict,
        ]:
            return cast(value_type, provided_value)

        if value_type != inspect.Parameter.empty:
            ret = value_type(provided_value)

        return ret

    @staticmethod
    @traverse_datastructures
    def serialize(obj):
        def is_json_serializable(v):
            try:
                json.dumps(v)
                return True
            except TypeError:
                return False

        if is_json_serializable(obj):
            return obj

        serialized = dill.dumps(obj)
        encoded = base64.b64encode(serialized).decode("utf-8")
        return encoded

    @staticmethod
    @traverse_datastructures
    def deserialize(serialized):
        try:
            decoded = base64.b64decode(serialized.encode("utf-8"))
            deserialized = dill.loads(decoded)
            return deserialized
        except:
            return serialized
