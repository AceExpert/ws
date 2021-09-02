import websockets

class WBSProtocol(websockets.WebSocketServerProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    async def send_message(self, data:dict):
        try:
            await self.send(str(dict(data)))
        except ValueError:
            raise ValueError(f"\"data\" parameter expects a dictionary or a dictionary convertable object. Got {type(data).__name__}")