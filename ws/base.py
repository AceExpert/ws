import typing
from typing import overload

from .utils.converters import event
from .utils import enforce_type
from .models import Object

class BaseSocket:
    def __init__(self):
        self.listeners: Object = Object({
            'message':[],
            'connect':[],
            'ready':[],
            'close':[],
            'disconnect': [],
        })
    @overload
    def on(self, event: str):
        ...
    @enforce_type
    def on(self, evnt: event):
        def decorator(coro: typing.Coroutine):
            if not self.listeners[evnt]: 
                self.listeners[evnt] = [coro]
            else: 
                self.listeners[evnt].append(coro)
        return decorator
    def event(self, coro: typing.Coroutine):
        if coro.__name__.startswith("on_"): self.listeners[coro.__name__[3:]].append(coro) 
