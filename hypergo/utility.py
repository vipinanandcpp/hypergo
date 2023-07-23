import base64
import hashlib
import inspect
import json
import types
from typing import Any, Dict, Mapping, Union, cast, get_origin

import dill
import glom
import pydash
import yaml

from hypergo.custom_types import JsonDict, JsonType, TypedDictType


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
    def json_serialize(obj: Dict[str, Any]) -> JsonDict:
        ret: JsonDict = {}

        if isinstance(obj, (list, tuple)):
            ret = [Utility.json_serialize(item) for item in obj]
        elif isinstance(obj, dict):
            ret = {str(key): Utility.json_serialize(value) for key, value in obj.items()}
        elif isinstance(obj, types.FunctionType):
            serialized_function = dill.dumps(obj)
            encoded_function = base64.b64encode(serialized_function).decode("utf-8")
            ret = {"__type__": "function", "__dill__": encoded_function}
        elif hasattr(obj, "__dict__"):
            serialized_obj = {}
            for key, value in obj.__dict__.items():
                serialized_obj[key] = Utility.json_serialize(value)
            ret = {
                "__type__": "instance",
                "__class__": obj.__class__.__name__,
                "__module__": obj.__class__.__module__,
                "__dict__": serialized_obj,
            }
        else:
            ret = obj
        return ret

    @staticmethod
    def json_deserialize(serialized: JsonDict) -> Dict[str, Any]:
        ret: Dict[str, Any] = {}

        if isinstance(serialized, list):
            ret = [Utility.json_deserialize(item) for item in serialized]
        elif isinstance(serialized, dict):
            if "__type__" in serialized:
                if serialized["__type__"] == "function":
                    encoded_function: JsonType = serialized["__dill__"]

                    # Ensure encoded_function is of the correct type
                    if isinstance(encoded_function, str):
                        encoded_function_bytes = encoded_function.encode("utf-8")
                    elif isinstance(encoded_function, (bytes, bytearray, memoryview)):
                        encoded_function_bytes = encoded_function
                    else:
                        raise ValueError("encoded_function must be a string or bytes-like object")

                    serialized_function = base64.b64decode(encoded_function_bytes)
                    deserialized_function: Any = dill.loads(serialized_function)
                    ret = deserialized_function
                elif serialized["__type__"] == "instance":
                    class_module_name: str = str(serialized["__module__"])
                    class_module = __import__(class_module_name)
                    class_name: str = str(serialized["__class__"])
                    class_ = getattr(class_module, class_name)
                    instance: Any = class_()
                    for key, value in cast(Dict[str, Any], serialized["__dict__"]).items():
                        setattr(instance, key, Utility.json_deserialize(value))
                    ret = instance
            else:
                ret = {
                    str(Utility.json_deserialize(key)): Utility.json_deserialize(value)
                    for key, value in serialized.items()
                }
        else:
            ret = serialized

        return ret
