from typing import Any, Dict, Generator

from hypergo.config import Config
from hypergo.executor import Executor
from hypergo.message import Message


def execute(config: Dict[str, Any], message: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    executor: Executor = Executor(Config(config))
    for execution in executor.execute(Message(message)):
        yield execution.to_dict()


if __name__ == "__main__":
    message1: Dict[str, Any] = {"body": {"data_blob_path": "hypergo/csv_test_data.csv"}, "routingkey": "batch.csv"}
    print(str(message1))
    for message2 in execute({"namespace": "datalink", "name": "csvconverter", "package": "ldp-csv-to-json-converter", "lib_func": "csv_to_json_converter_appliance.__main__.csv_to_json_appliance", "input_keys": ["batch.csv"], "output_keys": ["batch.json"], "input_bindings": ["body.data_blob_path"], "output_bindings": ["body.json_data"]}, message1):
        print(str(message2))
        for message3 in execute({"namespace": "datalink", "name": "batchstreamer", "package": "ldp-batch-to-stream-producer", "lib_func": "batch_to_stream_producer_appliance.__main__.batch_to_stream", "input_keys": ["batch.json"], "output_keys": ["item.json"], "input_bindings": ["body.json_data"], "output_bindings": ["body.json_datum"]}, message2):
            print(str(message3))
