import typing

class ParameterConflict(Exception):
    def __init__(self, message: str, *, paramters: typing.List[str]):
        super().__init__(message)
        self.message = message
        self.parameter = paramters
    def __repr__(self) -> str:
        return f"{self.message}"
    def __str__(self) -> str:
        return self.__repr__()