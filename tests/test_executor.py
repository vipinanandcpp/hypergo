import inspect
import unittest
from typing import Any, Callable, List, Tuple, Union, get_origin
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def safecast(some_type: type) -> Callable[..., Any]:
    if some_type == inspect.Parameter.empty:
        return lambda value: value
    return get_origin(some_type) or some_type


class TestSafeCast(unittest.TestCase):
    def test_safecast(self) -> None:
        # Test casting None
        none_cast = safecast(type(None))
        self.assertIsNone(none_cast())

        # Test casting a string
        str_cast = safecast(str)
        self.assertEqual(str_cast("hello"), "hello")

        # Test casting a list of strings
        list_str_cast = safecast(List[str])
        self.assertEqual(list_str_cast(["hello", "world"]), ["hello", "world"])

        # Test casting a tuple of int and string
        tuple_cast = safecast(Tuple[int, str])
        self.assertEqual(tuple_cast((1, "hello")), (1, "hello"))

        # Test casting a union of int and float
        union_cast = safecast(Union[int, float])
        self.assertEqual(union_cast(42), 42)
        self.assertEqual(union_cast(3.14), 3.14)

        # Test casting a custom class
        class MyClass:
            pass

        class_cast = safecast(MyClass)
        obj = MyClass()
        self.assertIs(class_cast(obj), obj)

        # Test casting a callable
        def my_function(x: int, y: int) -> int:
            return x + y

        callable_cast = safecast(Callable[[int, int], int])
        self.assertIs(callable_cast(my_function), my_function)

        # Test casting a parameter with a default value
        def my_function2(x: int, y: str = "default") -> None:
            pass

        param_cast = safecast(inspect.Parameter(str, inspect.Parameter.empty))
        self.assertEqual(param_cast("hello"), "hello")
        self.assertIsNone(param_cast(inspect.Parameter.empty))


if __name__ == "__main__":
    unittest.main()
