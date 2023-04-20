from hypergo.config import ConfigType
from hypergo.custom_types import TypedDictType
from hypergo.message import MessageType


class ContextType(TypedDictType):
    message: MessageType
    config: ConfigType
