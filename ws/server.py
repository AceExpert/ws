from datetime import datetime
import typing, websockets, asyncio, json
from json.decoder import JSONDecodeError
from websockets import ConnectionClosedError

from .base import BaseSocket
from .models.message import Message, Object
from .wsprotocols import WSSProtocol
from .collector import EventCollector

class ServerSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.listeners.message.append(self.on_message)
        self.listeners.connect.append(self.on_connect)
        self.listeners.ready.append(self.on_ready)
        self.listeners.disconnect.append(self.on_disconnect)
        self.listeners.close.append(self.on_close)
        self.clients = []
        self.disconnected_clients = []
    def listen(self, addr:str, port:int, ssl=None):
        self.address = addr
        self.port = port
        self.server = websockets.serve(self.__main, addr, port, create_protocol = WSSProtocol, ssl=ssl)
        self.loop.run_until_complete(self.server)
        self.loop.run_until_complete(asyncio.wait([coro() for coro in self.listeners.ready if type(coro) != tuple]))
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
                message_cls: Message = Message(data=data, websocket=websocket, created_at=datetime.utcnow())
                self.loop.create_task(asyncio.wait(
                     [coro(message_cls) for coro in self.listeners.message]+[self.__collector_verifier(futures, 'message', message_cls) 
                     for futures in self.listeners.message_collector
                    ]))
        except ConnectionClosedError as e:
            self.clients.remove(websocket)
            self.disconnected_clients.append({websocket: Object({'code': e.code, 'reason': e.reason, 'disconnected': True})})
            await asyncio.wait([coro(websocket, e.code, e.reason) for coro in self.listeners.disconnect]+[
                     self.__collector_verifier(futures, 'disconnect', e.code, e.reason) 
                     for futures in self.listeners.disconnect_collector
                    ])
            return e
    async def __on_connect(self, client, path):
        await asyncio.wait([coro(client, path) for coro in self.listeners.connect]+[self.__collector_verifier(futures, 'connect', client, path) 
                     for futures in self.listeners.connect_collector
                    ])
    async def on_connect(self, client, path):
        pass
    async def on_disconnect(self, client, code, reason):
        pass
    async def on_close(self, client, code, reason):
        pass
    async def on_ready(self):
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
    async def __main(self, websocket, path):
        self.clients.append(websocket)
        self.loop.create_task(self.__on_connect(websocket, path))
        done, pending = await asyncio.wait([self.__message_consumer(websocket)], return_when=asyncio.ALL_COMPLETED)
        if ConnectionClosedError in [type(ret.result()) for ret in done]: return
        self.clients.remove(websocket)
        self.disconnected_clients.append({websocket: Object({'code': websocket.close_code, 'reason': websocket.close_reason, 'disconnected': True})})
        await asyncio.wait([coro(websocket, websocket.close_code, websocket.close_reason) for coro in self.listeners.close]+[
                     self.__collector_verifier(futures, 'close', websocket, websocket.close_code, websocket.close_reason) 
                     for futures in self.listeners.close_collector
                    ])
    async def send(self, client, content: typing.Any = None, *, data: dict = None):
        await client.send(content=content, data=data)
    async def close(self, client, *, code: int = 1000, reason: str = ''):
        await client.close(code=code, reason=reason)