import typing, websockets, asyncio

from .base import BaseSocket

class ServerSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.listeners = {'message':[self.on_message], 'connect':[self.on_connect]}
        self.connections = set()
    def listen(self, addr:str, port:int):
        self.server = websockets.serve(self.__main, addr, port)
        self.loop.run_until_complete(self.server)
        self.loop.run_forever()
    async def on_message(self, message, websocket: websockets.WebSocketServerProtocol):
        pass
    async def __message_consumer(self, websocket: websockets.WebSocketServerProtocol):
        async for message in websocket:
            await asyncio.wait([coro(message, websocket) for coro in self.listeners['message']])
    async def __on_connect(self, websocket, path):
        await asyncio.wait([coro(websocket, path) for coro in self.listeners['connect']])
    async def on_connect(self, websocket, path):
        pass
    async def __main(self, websocket: websockets.WebSocketServerProtocol, path):
        self.connections.add(websocket)
        await asyncio.wait([self.__message_consumer(websocket),
                            self.__on_connect(websocket, path)
                            ])
    async def send(self, websocket: websockets.WebSocketServerProtocol, message:typing.Union[str, bytes, bytearray]):
        await websocket.send(message)
    async def recv(self, websocket: websockets.WebSocketServerProtocol):
        return await websocket.recv()