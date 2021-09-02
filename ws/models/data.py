import typing

class WebData:
    def __init__(self, data: dict):
        self.__data = data
    def __repr__(self) -> str:
        return str(self.__data)
    def __str__(self) -> str:
        return self.__repr__()
    def __getattr__(self, key):
        try:
            return self.__data[key]
        except KeyError as e:
            raise AttributeError(e)
    def __getitem__(self, key):
        return self.__data[key]
    def __setattr__(self, name: str, value: typing.Any) -> None:
        self.__data[name] = value
    def __setitem__(self, name: typing.Any, value: typing.Any) -> None:
        self.__data[name] = value
    def get(self, key: typing.Any, default: typing.Any = None):
        return self.__data.get(key, default)
    def set(self, key: typing.Any, value: typing.Any) -> bool:
        self.__data[key] = value
        return True
    def __delattr__(self, name: str):
        self.__data.pop(name)
    def __delitem__(self, key: typing.Any):
        self.__data.pop(key)
    def __iter__(self):
        for key, value in self.__data:
            yield (key, value)
    def items(self):
        return self.__iter__()
    def pop(self, key: typing.Any) -> typing.Any:
        return self.__data.pop(key)
    