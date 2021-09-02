from datetime import datetime
import typing, websockets, asyncio, ast

from .base import BaseSocket
from .models.message import Message
from .models.wbprotocol import WBSProtocol

class ServerSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.listeners['message'].append(self.on_message)
        self.listeners['connect'].append(self.on_connect)
        self.listeners['ready'].append(self.on_ready)
        self.connections = []
    def listen(self, addr:str, port:int):
        self.server = websockets.serve(self.__main, addr, port)
        self.loop.run_until_complete(self.server)
        self.loop.run_forever()
    async def on_message(self, message):
        pass
    async def __message_consumer(self, websocket: WBSProtocol):
        async for message in websocket:
            await asyncio.wait([coro(Message(data=ast.literal_eval(message), 
                                             socket=websocket, 
                                             created=datetime.utcnow())) for coro in self.listeners['message']])
    async def __on_connect(self, websocket, path):
        await asyncio.wait([coro(websocket, path) for coro in self.listeners['connect']])
    async def on_connect(self, websocket, path):
        pass
    async def on_ready():
        pass
    async def __main(self, websocket: WBSProtocol, path):
        self.connections.append(websocket)
        await asyncio.wait([self.__message_consumer(websocket),
                            self.__on_connect(websocket, path)
                            ])
    async def send(self, data: dict, websocket: WBSProtocol):
        await WBSProtocol(websocket).send_message(data)
    async def recv(self, websocket: WBSProtocol):
        return await websocket.recv()