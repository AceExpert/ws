import websockets

class WSCProtocol(websockets.WebSocketClientProtocol):
    def __init__(self, *args, **kwargs):
        """
            A subclass of WebSocketClientProtocol to provide extended send and receive functionalities. 
        """
        super().__init__(*args, **kwargs)
    async def send(self, data:dict):
        try:
            await super().send(str(dict(data)))
        except ValueError:
            raise ValueError(f"\"data\" parameter expects a dictionary or a dictionary convertable object. Got {type(data).__name__}")
