import unittest
from unittest.mock import MagicMock

from typing import Any, Dict, Mapping, Union
from hypergo.custom_types import TypedDictType
from hypergo.utility import Utility

import glom
import json
import yaml

class TestUtility(unittest.TestCase):
    def test_deep_get(self) -> None:
        # Test when key exists in dictionary
        input_dict: Dict[str, Dict[str, int]] = {"a": {"b": 1}}
        key: str = "a.b"
        expected_output: int = 1
        self.assertEqual(Utility.deep_get(input_dict, key), expected_output)

        # Test when key does not exist in dictionary
        input_dict: Dict[str, Dict[str, int]] = {"a": {"b": 1}}
        key: str = "a.c"
        with self.assertRaises(glom.PathAccessError):
            Utility.deep_get(input_dict, key)

    def test_deep_set(self) -> None:
        # Test when key exists in dictionary
        input_dict: Dict[str, Dict[str, int]] = {"a": {"b": 1}}
        key: str = "a.b"
        val: int = 2
        expected_output: Dict[str, Dict[str, int]] = {"a": {"b": 2}}
        Utility.deep_set(input_dict, key, val)
        self.assertEqual(input_dict, expected_output)

        # Test when key does not exist in dictionary
        input_dict: Dict[str, Dict[str, int]] = {"a": {"b": 1}}
        key: str = "a.c"
        val: int = 2
        expected_output: Dict[str, Dict[str, int]] = {"a": {"b": 1, "c": 2}}
        Utility.deep_set(input_dict, key, val)
        self.assertEqual(input_dict, expected_output)

    def test_yaml_read(self) -> None:
        # Mock the yaml.safe_load method
        yaml.safe_load = MagicMock(return_value={"a": 1})
        file_name: str = "tests/test.yaml"
        expected_output: Dict[str, int] = {"a": 1}
        self.assertEqual(Utility.yaml_read(file_name), expected_output)

    def test_yaml_write(self) -> None:
        # TODO: Implement test case for yaml_write method
        pass

    def test_json_read(self) -> None:
        # Mock the json.load method
        json.load = MagicMock(return_value={"a": 1})
        file_name: str = "tests/test.json"
        expected_output: Dict[str, int] = {"a": 1}
        self.assertEqual(Utility.json_read(file_name), expected_output)

    def test_json_write(self) -> None:
        # TODO: Implement test case for json_write method
        pass

    def test_hash(self) -> None:
        content: str = "test content"
        expected_output: str = "9473fdd0d880a43c21b7778d34872157"
        self.assertEqual(Utility.hash(content), expected_output)

    def test_safecast(self) -> None:
        # Test for int type
        expected_output: int = 1
        provided_value: Union[int, float, str] = 1
        value_type: type[int] = int
        self.assertEqual(Utility.safecast(value_type, provided_value), expected_output)

        # Test for float type
        expected_output: float = 1.0
        provided_value: Union[int, float, str] = 1
        value_type: type[float] = float
        self.assertEqual(Utility.safecast(value_type, provided_value), expected_output)

        # Test for unsupported type
        expected_output: str = "unsupported"
        provided_value: Union[int, float, str] = "unsupported"
        value_type: Union[type[int], type[float]] = str
        self.assertEqual(Utility.safecast(value_type, provided_value), expected_output)

if __name__ == '__main__':
    # Run the unit tests
    unittest.main()