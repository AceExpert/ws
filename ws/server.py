from datetime import datetime
import typing, websockets, asyncio, ast

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
    async def __message_consumer(self, websocket: WSSProtocol):
        async for message in websocket:
            await asyncio.wait([coro(Message(data=ast.literal_eval(message), 
                                             websocket=websocket, 
                                             created_at=datetime.utcnow())) for coro in self.listeners['message']])
    async def __on_connect(self, websocket: WSSProtocol, path):
        await asyncio.wait([coro(websocket, path) for coro in self.listeners['connect']])
    async def on_connect(self, websocket, path):
        pass
    async def on_ready(self):
        pass
    async def __main(self, websocket: WSSProtocol, path):
        self.clients.append(websocket)
        await asyncio.wait([self.__message_consumer(websocket),
                            self.__on_connect(websocket, path)
                            ])
    async def send(self, data: dict, client: WSSProtocol):
        await client.send(data)
    async def recv(self, client: WSSProtocol):
        return await client.recv()