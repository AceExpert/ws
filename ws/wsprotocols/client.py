import websockets, typing, json
from ..exceptions import ParameterConflict

class WSCProtocol(websockets.WebSocketClientProtocol):
    def __init__(self, *args, **kwargs):
        """
            A subclass of WebSocketClientProtocol to provide extended send and receive functionalities. 
        """
        super().__init__(*args, **kwargs)
    async def send(self, content: typing.Union[str, bytes, bytearray, typing.List[typing.Any]] = None, *, data: dict = None):
        if not data and not content:
            raise TypeError("Missing either both of \"data\" or \"content\" parameter. Any one is required.")
        if data and content:
            raise ParameterConflict("Got values for both data and content. Expected anyone.", paramters=['data', 'content'])
        if not data:
            await super().send(content)
            return
        try:
            await super().send(json.dumps((dict(data))))
        except ValueError:
            raise ValueError(f"\"data\" parameter expects a dictionary or a dictionary convertable object. Got {type(data).__name__}")
        except TypeError as e:
            raise TypeError(". ".join(list(e.args)))
    def __repr__(self) -> str:
        return f"<WSClientProtocol remote_address={self.remote_address} local_address={self.local_address}>"
    def __str__(self) -> str:
        return self.__repr__()
