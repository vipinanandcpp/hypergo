import unittest
from hypergo.utility import Utility

class TestUtility(unittest.TestCase):

    def test_scalar_values(self):
        # Test scalar values (str, int, float, bool, None)
        test_values = [
            ("Hello, World!", "Hello, World!"),
            (42, 42),
            (3.14, 3.14),
            (True, True),
            (None, None),
        ]
        for py_value, json_value in test_values:
            with self.subTest(py_value=py_value):
                self.assertEqual(Utility.json_deserialize(Utility.json_serialize(py_value)), json_value)

    def test_nested_dicts_and_lists(self):
        # Test nested dicts and lists
        test_dict = {
            "name": "John",
            "age": 30,
            "address": {
                "city": "New York",
                "zip_code": 10001
            },
            "hobbies": ["Reading", "Hiking"]
        }

        json_dict = Utility.json_serialize(test_dict)
        restored_dict = Utility.json_deserialize(json_dict)
        self.assertEqual(restored_dict, test_dict)

    def test_singular_function(self):
        # Test a singular function
        def add(x, y):
            return x + y

        json_func = Utility.json_serialize(add)
        restored_func = Utility.json_deserialize(json_func)

        self.assertEqual(restored_func(3, 4), 7)

    def test_singular_class(self):
        # Test a singular class
        class TestClass:
            def __init__(self, name):
                self.name = name

            def greet(self):
                return f"Hello, {self.name}!"

        instance = TestClass("Alice")
        json_instance = Utility.json_serialize(instance)
        restored_instance = Utility.json_deserialize(json_instance)

        self.assertEqual(restored_instance.greet(), "Hello, Alice!")

if __name__ == "__main__":
    unittest.main()
