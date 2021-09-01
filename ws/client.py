import websockets, typing, asyncio

from .base import BaseSocket

class ClientSocket(BaseSocket):
    def __init__(self, ws:str):
        super().__init__()
        self.__ws = ws
        self.loop = asyncio.get_event_loop()
        self.listeners = {'message':[self.on_message], 'connect':[self.on_connect]}
        self.connection = None
    def connect(self):
        self.loop.run_until_complete(self.__main())
        self.loop.run_forever()
    async def on_message(self, message):
        pass
    async def __message_consumer(self):
        async for message in self.connection:
            await asyncio.wait([coro(message) for coro in self.listeners['message']])
    async def __on_connect(self):
        await asyncio.wait([coro() for coro in self.listeners['connect']])
    async def on_connect(self):
        pass
    async def __main(self):
        self.connection = await websockets.connect(self.__ws)
        await asyncio.wait([self.__message_consumer(),
                            self.__on_connect()
                            ])
    async def send(self, message:typing.Union[str, bytes, bytearray]):
        await self.connection.send(message)
    async def recv(self):
        return await self.connection.recv()
