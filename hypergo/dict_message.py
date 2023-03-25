import glom
from hypergo.types import TypeDict
from hypergo.message import Message


class DictMessage(Message):
    def get_data(self) -> TypeDict:
        return self._message["content"]

    def get_meta(self) -> TypeDict:
        return self._message["meta"]

    def get_rk(self) -> str:
        return str(glom.glom(self._message, "meta.filter"))

    def send(self, message: str) -> None:
        print(message)
