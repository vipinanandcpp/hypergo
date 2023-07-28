from typing import Callable, Generator, TypeVar

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
        def wrapper(func: Callable[..., Generator[T, None, None]]) -> Callable[..., Generator[T, None, None]]:
            return lambda self, data: (
                Utility.compress(result, key) for result in func(self, Utility.uncompress(data, key))
            )

        return wrapper
