from datetime import datetime
import typing, websockets, asyncio, json
from json.decoder import JSONDecodeError
from websockets import ConnectionClosedError, ConnectionClosedOK

from .base import BaseSocket
from .models.message import Message, Object
from .wsprotocols import WSSProtocol


class ServerSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.listeners.message.append(self.on_message)
        self.listeners.connect.append(self.on_connect)
        self.listeners.ready.append(self.on_ready)
        self.listeners.disconnect.append(self.on_disconnect)
        self.listeners.close.append(self.on_close)
        self.clients = []
        self.disconnected_clients = []
    def listen(self, addr:str, port:int):
        self.address = addr
        self.port = port
        self.server = websockets.serve(self.__main, addr, port, create_protocol = WSSProtocol)
        self.loop.run_until_complete(self.server)
        self.loop.run_until_complete(asyncio.wait([coro() for coro in self.listeners.ready]))
        self.loop.run_forever()
    async def on_message(self, message):
        pass
    async def __message_consumer(self, websocket):
        try:
            async for message in websocket:             
                try:
                    data = json.loads(message)
                except JSONDecodeError:
                    data = message
                await asyncio.wait([coro(Message(data=data, 
                                                websocket=websocket, 
                                                created_at=datetime.utcnow())) for coro in self.listeners.message])
        except ConnectionClosedError as e:
            self.clients.remove(websocket)
            self.disconnected_clients.append({websocket: Object({'code': e.code, 'reason': e.reason, 'disconnected': True})})
            await asyncio.wait([coro(websocket, e.code, e.reason) for coro in self.listeners.disconnect])
            return e
    async def __on_connect(self, client, path):
        await asyncio.wait([coro(client, path) for coro in self.listeners.connect])
    async def on_connect(self, client, path):
        pass
    async def on_disconnect(self, client, code, reason):
        pass
    async def on_close(self, client, code, reason):
        pass
    async def on_ready(self):
        pass
    async def __main(self, websocket, path):
        self.clients.append(websocket)
        done, pending = await asyncio.wait([self.__message_consumer(websocket),
                            self.__on_connect(websocket, path)
                            ], return_when=asyncio.ALL_COMPLETED)
        if ConnectionClosedError in [type(ret) for ret in done]: return
        self.clients.remove(websocket)
        self.disconnected_clients.append({websocket: Object({'code': websocket.close_code, 'reason': websocket.close_reason, 'disconnected': True})})
        await asyncio.wait([coro(websocket, websocket.close_code, websocket.close_reason) for coro in self.listeners.close])
    async def send(self, client, content: typing.Any = None, *, data: dict = None):
        await client.send(content=content, data=data)
    async def close(self, client, *, code: int, reason: str = ''):
        await client.close(code=code, reason=reason)