from hypergo.utility import Utility


class Transform:
    @staticmethod
    def serialization(func):
        return lambda self, message: (
            Utility.json_serialize(result) for result in func(self, Utility.json_deserialize(message))
        )
