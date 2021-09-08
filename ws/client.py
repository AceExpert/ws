from datetime import datetime
import websockets, typing, asyncio, json
from json.decoder import JSONDecodeError
from websockets import ConnectionClosedError

from .base import BaseSocket
from .models import Message, Object
from .wsprotocols import WSCProtocol
from .collector import EventCollector

class ClientSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.listeners['message'].append(self.on_message)
        self.listeners['connect'].append(self.on_connect)
        self.listeners['disconnect'].append(self.on_disconnect)
        self.listeners.close.append(self.on_close)
        self.connection = None
        self.disconnection = None
    def connect(self, uri: str, ssl=None):
        self.loop.run_until_complete(self.__main(uri, ssl))
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
                message_cls: Message = Message(data=data, websocket=self.connection, created_at=datetime.utcnow())
                self.loop.create_task(asyncio.wait(
                    [coro(message_cls) for coro in self.listeners['message']]+[self.__collector_verifier(futures, 'message', message_cls) 
                     for futures in self.listeners.message_collector
                    ]
                ))
        except ConnectionClosedError as e:
            self.disconnection = Object({'code': e.code, 'reason': e.reason, 'disconnected': True})
            await asyncio.wait([coro(e.code, e.reason) for coro in self.listeners.disconnect]+[
                     self.__collector_verifier(futures, 'disconnect', e.code, e.reason) 
                     for futures in self.listeners.disconnect_collector
                    ]
            )
            return e
    async def __on_connect(self):
        await asyncio.wait([coro() for coro in self.listeners['connect']])
    async def on_connect(self):
        pass
    async def on_disconnect(self, code, reason):
        pass
    async def on_close(self, code, reason):
        pass
    async def __collector_verifier(self, futures, event, *event_data):
        if futures[1](*event_data):
            try:
                futures[0].set_result(event_data[0] if len(event_data) == 1 else event_data)
                self.listeners[f"{event}_collector"].remove(futures)
            except asyncio.exceptions.InvalidStateError:
                try:
                    self.listeners[f"{event}_collector"].remove(futures)
                except ValueError:
                    pass
            except ValueError:
                pass
    def collector(self, time: float):
        return EventCollector(websocket=self, time=time)
    async def __main(self, uri, ssl=None):
        self.connection = await websockets.connect(uri, create_protocol=WSCProtocol, ssl=ssl)
        self.loop.create_task(self.__on_connect())
        done, pending = await asyncio.wait([self.__message_consumer()], return_when=asyncio.ALL_COMPLETED)
        if ConnectionClosedError in [type(ret.result()) for ret in done]: return
        self.disconnection = Object({'code': self.connection.close_code, 'reason': self.connection.close_reason, 'disconnected': True})
        await asyncio.wait([coro(self.connection.close_code, self.connection.close_reason) for coro in self.listeners.close]+[
                     self.__collector_verifier(futures, 'close', self.connection.close_code, self.connection.close_reason) 
                     for futures in self.listeners.close_collector
                    ])
    async def send(self, content: typing.Any = None, *, data: dict = None):
        await self.connection.send(content=content, data=data)
    async def close(self, code: int = 1000, reason: str = ''):
        await self.connection.close(code=code, reason=reason)
