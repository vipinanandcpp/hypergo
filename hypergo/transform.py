from hypergo.utility import Utility


class Transform:
    @staticmethod
    def serialization(func):
        return lambda self, message: (
            Utility.serialize(result) for result in func(self, Utility.deserialize(message))
        )
