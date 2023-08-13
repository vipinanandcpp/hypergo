# import json

from typing import Any, Dict, Tuple, Union


class Logger:
    @staticmethod
    def warning(*args: Union[Tuple[Any, ...], Any], **kwargs: Dict[str, Any]) -> None:
        pass
        # print(json.dumps(*args))
