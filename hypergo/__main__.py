from hypergo.config import Config
from hypergo.executor import Executor
from hypergo.message import Message


def test01(config, message):
    executor = Executor(Config(config))
    for execution in executor.execute(Message(message)):
        print(str(execution.to_dict()))


if __name__ == "__main__":
    test01({"namespace": "datalink", "name": "batchstreamer", "package": "ldp-batch-to-stream-producer", "lib_func": "batch_to_stream_producer_appliance.__main__.batch_to_stream", "input_keys": ["batch.json"], "output_keys": ["item.json"], "input_bindings": ["body.json_data"], "output_bindings": ["body.json_datum"]}, {"body": {"json_data": [{"a": "1"}, {"a": 2}]}, "routingkey": "batch.json"})
