import typing

from .utils.converters import event

class BaseSocket:
    def __init__(self):
        self.listeners: typing.Dict[str, typing.List[typing.Coroutine]] = {
            'message':[],
            'connect':[],
            'ready':[],
            'close':[],
            'disconnect': [],
        }
    def on(self, event: event):
        def decorator(coro: typing.Coroutine):
            if not self.listeners[event]: 
                self.listeners[event] = [coro]
            else: 
                self.listeners[event].append(coro)
        return decorator