from datetime import datetime
import websockets, typing, asyncio, json
from json.decoder import JSONDecodeError
from websockets import ConnectionClosedError

from .base import BaseSocket
from .models import Message, Object
from .wsprotocols import WSCProtocol

class ClientSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.listeners['message'].append(self.on_message)
        self.listeners['connect'].append(self.on_connect)
        self.listeners['disconnect'].append(self.on_disconnect)
        self.listeners.close.append(self.on_close)
        self.connection = None
        self.disconnection = None
    def connect(self, ws_url: str):
        self.loop.run_until_complete(self.__main(ws_url))
        self.loop.run_forever()
    async def on_message(self, message):
        pass
    async def __message_consumer(self):
        try:
            async for message in self.connection:
                try:
                    data = json.loads(message)
                except JSONDecodeError:
                    data = message
                await asyncio.wait([coro(Message(data=data,
                                                 websocket=self.connection,
                                                 created_at=datetime.utcnow()
                                                )) for coro in self.listeners['message']])
        except ConnectionClosedError as e:
            self.disconnection = Object({'code': e.code, 'reason': e.reason, 'disconnected': True})
            await asyncio.wait([coro(e.code, e.reason) for coro in self.listeners.disconnect])
            return e
    async def __on_connect(self):
        await asyncio.wait([coro() for coro in self.listeners['connect']])
    async def on_connect(self):
        pass
    async def on_disconnect(self, code, reason):
        pass
    async def on_close(self, code, reason):
        pass
    async def __main(self, ws_url):
        self.connection = await websockets.connect(ws_url, create_protocol=WSCProtocol)
        done, pending = await asyncio.wait([self.__message_consumer(),
                            self.__on_connect()
                            ], return_when=asyncio.ALL_COMPLETED)
        if ConnectionClosedError in [type(ret) for ret in done]: return
        self.disconnection = Object({'code': self.connection.close_code, 'reason': self.connection.close_reason, 'disconnected': True})
        await asyncio.wait([coro(self.connection.close_code, self.connection.close_reason) for coro in self.listeners.close])
    async def send(self, content: typing.Any = None, *, data: dict = None):
        await self.connection.send(content=content, data=data)
    async def close(self, code: int, reason: str = ''):
        await self.connection.close(code=code, reason=reason)
