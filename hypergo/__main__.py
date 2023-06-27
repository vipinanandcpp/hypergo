from typing import Generator

from hypergo.config import ConfigType
from hypergo.executor import Executor
from hypergo.local_storage import LocalStorage
from hypergo.message import MessageType
from hypergo.storage import Storage


def execute(config: ConfigType, message: MessageType) -> Generator[MessageType, None, None]:
    storage: Storage = LocalStorage()
    executor: Executor = Executor(config, storage)
    for execution in executor.execute(message):
        yield execution


# fmt: off
if __name__ == "__main__":
    message1: MessageType = {
        "body": {"data_blob_path": "hypergo/csv_test_data.csv"},
        "routingkey": "batch.csv"
    }
    print(str(message1))
    for message2 in execute(
            {
                "namespace": "datalink",
                "name": "csvconverter",
                "package": "ldp-csv-to-json-converter",
                "lib_func": "csv_to_json_converter_appliance.__main__.csv_to_json_appliance",
                "input_keys": ["batch.csv"],
                "output_keys": ["batch.json"],
                "input_bindings": ["message.body.data_blob_path"],
                "output_bindings": ["message.body.json_data"],
                "output_operations": ["pass_by_reference"]},
            message1):
        print(str(message2))
        for message3 in execute(
                {
                    "namespace": "datalink",
                    "name": "deltaproducer",
                    "package": "ldp-delta-producer",
                    "lib_func": "delta_producer_appliance.__main__.produce_json_deltas",
                    "input_keys": ["batch.json"],
                    "output_keys": ["item.json"],
                    "input_bindings": ["message.body.json_data"],
                    "output_bindings": ["message.body.json_data"],
                    "input_operations": ["pass_by_reference"]},
                message2):
            print(str(message3))
            for message4 in execute(
                    {
                        "namespace": "datalink",
                        "name": "batchstreamer",
                        "package": "ldp-batch-to-stream-producer",
                        "lib_func": "batch_to_stream_producer_appliance.__main__.batch_to_stream",
                        "input_keys": ["item.json"],
                        "output_keys": ["xx.json"],
                        "input_bindings": ["message.body.json_data"],
                        "output_bindings": ["message.body.json_datum"]},
                    message3):
                print(str(message4))

    new_message_1: MessageType = {
        "body": {"name": "Chris", "company": "LinkLogistics"},
        "routingkey": "a.b.c.x"
    }
    for sdk_message_1 in execute({
        "namespace": "datalink",
        "name": "batchstreamer",
        "package": "ldp-batch-to-stream-producer",
        "lib_func": "batch_to_stream_producer_appliance.__main__.batch_to_stream",
        "input_keys": ["a.b.c", "a.b.d", "a.b", "a"],
        "output_keys": ["y.h.?.?"],
        "input_bindings": ["message.body"],
        "output_bindings": ["message.body"]
    }, new_message_1):
        print(sdk_message_1["routingkey"])

    new_message_2: MessageType = {"body":{}, "routingkey":"link.db.query.specleasing.scheduled.select_query"}
    for sdk_message in execute({
        "namespace": "datalink",
        "name": "snowflakedbexecutor",
        "package": "ldp-db-executor",
        "lib_func": "dbexecutor_appliance.snowflake_db_executor_appliance.__main__.execute",
        "input_keys": ["link.db.query"],
        "output_keys": ["?.db.result.link.json"],
        "input_bindings": ["config.custom_configurations.?"],
        "output_bindings": ["message.body.snowflake.db.record"],
        "custom_configurations":{"specleasing.select_query": "SELECT * FROM DP_LNK_DEV_DB.DP_LNK_ENTITIES.VW_UNIT_VALUATIONS LIMIT 10;"}}, 
                                 new_message_2):
        print(sdk_message)

# fmt: on
