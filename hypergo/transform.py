from typing import Any, Callable, Generator, TypeVar, cast

from hypergo.custom_types import JsonDict, JsonType
from hypergo.storage import Storage
from hypergo.utility import Utility

T = TypeVar("T")


class Transform:
    @staticmethod
    def serialization(func: Callable[..., Generator[T, None, None]]) -> Callable[..., Generator[T, None, None]]:
        return lambda self, data: (Utility.serialize(result) for result in func(self, Utility.deserialize(data)))

    @staticmethod
    def compression(
        key: str,
    ) -> Callable[[Callable[..., Generator[T, None, None]]], Callable[..., Generator[T, None, None]]]:
        def decorator(func: Callable[..., Generator[T, None, None]]) -> Callable[..., Generator[T, None, None]]:
            def wrapper(self: Any, data: T) -> Generator[T, None, None]:
                if "compression" in Utility.deep_get(self.config, "input_operations"):
                    data = Utility.uncompress(data, key)

                for result in func(self, data):
                    if "compression" in Utility.deep_get(self.config, "output_operations"):
                        result = Utility.compress(result, key)
                    yield result

            return wrapper

        return decorator

    @staticmethod
    def pass_by_reference(
        func: Callable[..., Generator[T, None, None]]
    ) -> Callable[..., Generator[JsonDict, None, None]]:
        def wrapper(self: Any, data: T) -> Generator[JsonDict, None, None]:
            storage: Storage = self.storage.use_sub_path("passbyreference")
            the_data: JsonType = cast(JsonType, data)
            if "pass_by_reference" in Utility.deep_get(self.config, "input_operations"):
                storagekey: str = Utility.deep_get(cast(JsonDict, data), "storagekey")
                the_data = Utility.objectify(storage.load(storagekey))
            for result in func(self, the_data):
                outmessage: JsonDict = cast(JsonDict, result)
                if "pass_by_reference" in Utility.deep_get(self.config, "output_operations"):
                    str_result = Utility.stringify(outmessage)
                    out_storagekey = Utility.hash(str_result)
                    storage.save(out_storagekey, str_result)
                    outmessage = {"storagekey": out_storagekey}
                yield outmessage

        return wrapper
