from message import Message
from typing import Dict, Any
import glom

class DictMessage(Message):
    def get_data(self) -> Dict[str, Any]:
        return self._message["content"]

    def get_meta(self) -> Dict[str, Any]:
        return self._message["meta"]

    def get_rk(self) -> str:
        return glom.glom(self._message, "meta.filter")
    
    def send(self, message: str) -> None:
        print(message)

