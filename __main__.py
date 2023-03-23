sample_payload = {
    "meta": {
        "filter": "a.b.c",
    },
    "content": {
        "primes": {
            "odds": {
                "first": "three",
                "second": "5",
                "third": "7"
            },
            "evens": {
            }
        },
        "fibonacci": {
            "odds": {
                "first": "1",
                "second": "3",
                "third": "5"
            },
            "evens": {
                "first": "two",
                "second": "8",
                "third": "34"
            }
        }
    }
}

from typing import Union, Dict, Any
import azure.functions as func
from message import Message

def host_function(message: Union[Dict[str, Any], func.ServiceBusMessage]) -> None:
    msg: Message = Message.create(message)
    msg.send(msg.consume())

if __name__ == "__main__":
    host_function(sample_payload)

# {
#   "scriptFile": "__init__.py",
#   "bindings": [
#     {
#       "name": "msg",
#       "type": "serviceBusTrigger",
#       "direction": "in",
#       "queueName": "inputqueue",
#       "connection": "AzureServiceBusConnectionString"
#     }
#   ]
# }


# import azure.functions as func
# import logging
# import json
# def main(msg: func.ServiceBusMessage):
#     logging.info('Python ServiceBus queue trigger processed message.')
#     result = json.dumps({
#         'message_id': msg.message_id,
#         'body': msg.get_body().decode('utf-8'),  DONE
#         'content_type': msg.content_type,
#         'expiration_time': msg.expiration_time,
#         'label': msg.label,
#         'partition_key': msg.partition_key,
#         'reply_to': msg.reply_to,
#         'reply_to_session_id': msg.reply_to_session_id,
#         'scheduled_enqueue_time': msg.scheduled_enqueue_time,
#         'session_id': msg.session_id,
#         'time_to_live': msg.time_to_live,
#         'to': msg.to,
#         'user_properties': msg.user_properties, DONE
#         'metadata' : msg.metadata
#     }, default=str)
#     logging.info(result)