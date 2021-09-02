import websockets, datetime, typing

from .data import WebData
from .wbprotocol import WBSProtocol

class Message:
    def __init__(self, data: dict, 
                       socket: typing.Union[WBSProtocol, websockets.WebSocketClientProtocol] = None, 
                       created: datetime.datetime = None):
        self.data: typing.Union[WebData, None] = WebData(data)
        self.author: typing.Union[WBSProtocol, websockets.WebSocketClientProtocol, None] = socket
        self.created_at: datetime.datetime = created
    