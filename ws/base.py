import typing

class BaseSocket:
    def __init__(self):
        self.listeners: typing.Dict[str, typing.List[typing.Coroutine]] = {
            'message':[],
            'connect':[],
            'ready':[],
            'close':[],
        }
    def on(self, event:str):
        def wrapper(coro: typing.Coroutine):
            if not self.listeners[event.lower()]:
                self.listeners[event.lower()] = [coro]
            else:
                self.listeners[event.lower()].append(coro)
        return wrapper