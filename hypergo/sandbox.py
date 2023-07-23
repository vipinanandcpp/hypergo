import dill
import json

from hypergo.utility import Utility

def do_substitution(value, data):
    def handle_str(string, data):
        match = re.match(r'^{([^}]+)}$', string)
        return Utility.deep_get(data, do_dynamic(match.group(1)), match.group(0)) if match else re.sub(r'{([^}]+)}', lambda match: str(Utility.deep_get(data, do_dynamic(match.group(1)), match.group(0))), string)

    return {
        str: handle_str,
        dict: lambda dic, data: {handle_str(key, data): do_substitution(dic, data) for key, dic in dic.items()},
        list: lambda lst, data: [do_substitution(lst, data) for lst in value]
    }.get(type(value), value)(value, data)



def dictify(func):
    def wrapper(value):
        return {
            dict: lambda d: {wrapper(k): wrapper(v) for k, v in d.items()},
            list: lambda l: [wrapper(i) for i in l]
        }.get(type(value), func)(value)

    return wrapper

@dictify
def json_serialize(value):
    print(f"Serialize {str(value)}")
    try:
        return json.dumps(value)
    except (TypeError, OverflowError):
        return dill.dumps(value)

@dictify
def json_deserialize(value):
    print(f"Deserialize {str(value)}")
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError, UnicodeDecodeError):
        return dill.loads(value)

@dictify
def reversify(value):
    if type(value) == str:
        return value[::-1]
    return value

def test():
    # fixture = get_fixture()
    # x = json_serialize(fixture)
    # y = json_deserialize(x)
    # print(f"{x}\n\n\n\n{y}")

    print(json_deserialize(get_serialized_fixture()))

def get_fixture():
    # Importing required modules for binary data and bytes
    import os

    # Sample function
    def sample_function(x):
        return x * x

    # Sample class
    class SampleClass:
        def __init__(self, name):
            self.name = name

        def greet(self):
            return f"Hello, {self.name}!"

    # Sample instance of a class
    sample_instance = SampleClass("Alice")

    # Sample binary data
    binary_data = os.urandom(10)

    # Expanded comprehensive dictionary
    return {
        "string": "Hello, world!",
        "integer": 42,
        "float": 3.14,
        "boolean": True,
        "list": [1, 2, 3, 4, 5],
        "tuple": (6, 7, 8),
        "set": {9, 10, 11},
        "str_address": "123 Main St. Suite 100 Chicago, IL",
        "dictionary": {
            "name": "John Doe",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "zip_code": "10001",
            },
        },
        "nested_list": [
            12,
            "nested string",
            [13, 14, 15],
            {"key": "value"},
            [{"nested_key": "nested_value"}],
        ],
        "nested_dict": {
            "key1": "value1",
            "key2": {
                "inner_key1": 16,
                "inner_key2": [17, 18, 19],
                "inner_key3": {
                    "inner_inner_key": "nested value",
                    "inner_inner_list": [20, 21, 22],
                },
            },
        },
        "empty_dict": {},
        "empty_list": [],
        "empty_set": set(),
        "empty_string": "",
        "none_value": None,
        "function": sample_function,  # Sample function
        "class": SampleClass,  # Sample class
        "instance": sample_instance,  # Sample instance of a class
        "binary_data": binary_data,  # Sample binary data
        "bytes": b"hello",  # Sample bytes
    }

def get_serialized_fixture():
    return Utility.serialize(get_fixture())
print(json.dumps(get_serialized_fixture(), indent=4))
# test()
