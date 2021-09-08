import typing, asyncio, inspect
from typing import overload

from .utils import to_event, enforce_type
from .models import Object
from .collector import EventCollector
from .exceptions import EventNotFound

class BaseSocket:
    def __init__(self):
        self.listeners: Object = Object({
            'message':[],
            'connect':[],
            'ready':[],
            'close':[],
            'disconnect': [],
            'message_collector': [],
            'connect_collector': [],
            'disconnect_collector':[],
            'close_collector': [],
        })
        self.events = ['message', 'connect', 'ready', 'close', 'disconnect']
        self.loop = asyncio.get_event_loop()
    @overload
    def on(self, event: str):
        ...
    @enforce_type
    def on(self, event: to_event):
        if event not in self.events:
            raise EventNotFound(f"There is no registerable event with the name \"{event}\".")
        def decorator(coro: typing.Coroutine):
            if not inspect.iscoroutinefunction(coro):
                raise TypeError(f"Expected a coroutine function found {type(coro).__name__}.")
            if not self.listeners[event]: 
                self.listeners[event] = [coro]
            else: 
                self.listeners[event].append(coro)
        return decorator
    def event(self, coro: typing.Coroutine):
        if not inspect.iscoroutinefunction(coro):
            raise TypeError(f"Expected a coroutine function found {type(coro).__name__}.")
        if coro.__name__.startswith("on_"): self.listeners[coro.__name__[3:]].append(coro)
    @overload
    def wait_for(self, event: str, *, 
                       check: typing.Optional[typing.Callable] = None, 
                       timeout: typing.Optional[float] = None):
        ...
    @enforce_type
    def wait_for(self, event: to_event, *, check = None, timeout: float = None):
        if event not in self.events: raise EventNotFound(f"There is no registerable event with the name \"{event}\".")
        future = self.loop.create_future()
        if check in [True, None, False]:
            check = lambda *args: True if check in [True, None] else False
        self.listeners[f"{event}_collector"].append((future, check))
        return asyncio.wait_for(future, timeout=timeout)
    @classmethod
    def Collector(websocket, time: float):
        return EventCollector(websocket=websocket, time=time)
    @overload
    def get_listeners(self, event: typing.Optional[str] = None) -> typing.Union[Object, typing.List[typing.Coroutine]]:
        ...
    def get_listeners(self, event: str = None):
        event = to_event(event)
        if event:
            if event not in self.events: raise EventNotFound(f"There is no registerable event with the name \"{event}\".")
            return self.listeners[event]
        else:
            return Object({event_name:listeners for event_name, listeners in self.listeners.items() if not event_name.endswith("_collector")})
