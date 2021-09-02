import websockets, datetime, typing

from .data import WebData
from .wbsprotocol import WBSProtocol

class Message:
    def __init__(self, data: dict, socket: WBSProtocol = None, created: datetime.datetime = None):
        self.data: typing.Union[WebData, None] = WebData(data.get('data', None)) if data.get('data', None) else None
        self.author: typing.Union[WBSProtocol, None] = socket
        self.created_at: datetime.datetime = created
    