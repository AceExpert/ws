import typing, asyncio
from typing import overload

from .utils import to_event, enforce_type
from .models import Object

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
        self.loop = asyncio.get_event_loop()
    @overload
    def on(self, event: str):
        ...
    @enforce_type
    def on(self, event: to_event):
        def decorator(coro: typing.Coroutine):
            if not self.listeners[event]: 
                self.listeners[event] = [coro]
            else: 
                self.listeners[event].append(coro)
        return decorator
    def event(self, coro: typing.Coroutine):
        if coro.__name__.startswith("on_"): self.listeners[coro.__name__[3:]].append(coro)
    @overload
    def wait_for(self, event: str, *, 
                       check: typing.Optional[typing.Callable] = None, 
                       timeout: typing.Optional[float] = None):
        ...
    @enforce_type
    def wait_for(self, event: to_event, *, check = None, timeout: float = None):
        future = self.loop.create_future()
        if check in [True, None, False]:
            check = lambda *args: True if check in [True, None] else False
        self.listeners[f"{event}_collector"].append((future, check))
        return asyncio.wait_for(future, timeout=timeout)
        
