import typing

class WebData(dict):
    def __init__(self, data: dict):
        super().__init__(data)
    def __getattr__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            raise AttributeError(e)
    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setitem__(name, value)
    def get(self, key: typing.Any, default: typing.Any = None):
        return super().get(key, default)
    def set(self, key: typing.Any, value: typing.Any) -> bool:
        super().__setitem__(key, value)
        return True
    def __delattr__(self, name: str):
        super().pop(name)
    def __delitem__(self, key: typing.Any):
        super().pop(key)
    def __iter__(self):
        for key, value in self.__data:
            yield (key, value)
    def items(self):
        return self.__iter__()