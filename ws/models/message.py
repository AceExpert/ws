import datetime, typing

from .data import Object
from ..wsprotocols import WSSProtocol, WSCProtocol

class Message:
    def __init__(self, data: typing.Any = {}, 
                       websocket: typing.Union[WSSProtocol, WSCProtocol] = None, 
                       created_at: datetime.datetime = None):
        self.data: typing.Any = Object(data) if type(data) == dict else data
        self.author: typing.Union[WSSProtocol, WSCProtocol, None] = websocket
        self.created_at: datetime.datetime = created_at
    def __repr__(self) -> str:
        return f"<Message {'message' if type(self.data) != Object else 'data'}={self.data} author={self.author} created_at={self.created_at}>"
    def __str__(self) -> str:
        return str(self.data)