import datetime, typing

from .data import WebSocketData
from ..wsprotocols import WSSProtocol, WSCProtocol

class Message:
    def __init__(self, data: typing.Any = {}, 
                       websocket: typing.Union[WSSProtocol, WSCProtocol] = None, 
                       created_at: datetime.datetime = None):
        self.data: typing.Any = WebSocketData(data) if type(data) == dict else data
        self.author: typing.Union[WSSProtocol, WSCProtocol, None] = websocket
        self.created_at: datetime.datetime = created_at
    