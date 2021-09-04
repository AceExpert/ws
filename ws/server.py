from datetime import datetime
import typing, websockets, asyncio, json
from json.decoder import JSONDecodeError

from .base import BaseSocket
from .models.message import Message
from .wsprotocols import WSSProtocol


class ServerSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.listeners['message'].append(self.on_message)
        self.listeners['connect'].append(self.on_connect)
        self.listeners['ready'].append(self.on_ready)
        self.clients = []
    def listen(self, addr:str, port:int):
        self.address = addr
        self.port = port
        self.server = websockets.serve(self.__main, addr, port, create_protocol = WSSProtocol)
        self.loop.run_until_complete(self.server)
        self.loop.run_until_complete(asyncio.wait([coro() for coro in self.listeners['ready']]))
        self.loop.run_forever()
    async def on_message(self, message):
        pass
    async def __message_consumer(self, websocket):
        async for message in websocket:
            try:
                data = json.loads(message)
            except JSONDecodeError:
                data = message
            await asyncio.wait([coro(Message(data=data, 
                                             websocket=websocket, 
                                             created_at=datetime.utcnow())) for coro in self.listeners['message']])
    async def __on_connect(self, client, path):
        await asyncio.wait([coro(client, path) for coro in self.listeners['connect']])
    async def on_connect(self, client, path):
        pass
    async def on_ready(self):
        pass
    async def __main(self, websocket, path):
        self.clients.append(websocket)
        await asyncio.wait([self.__message_consumer(websocket),
                            self.__on_connect(websocket, path)
                            ])
    async def send(self, data: typing.Any, client):
        await client.send(data)