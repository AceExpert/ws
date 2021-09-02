import websockets

class WBSProtocol(websockets.WebSocketServerProtocol):
    def __init__(self, wbs):
        super().__init__(wbs.ws_handler, wbs.ws_server)
        self.__wbs: websockets.WebSocketServerProtocol = wbs
    async def send_message(self, data:dict):
        try:
            await self.__wbs.send(str(dict(data)))
        except ValueError:
            raise ValueError(f"\"data\" parameter expects a dictionary or a dictionary convertable object. Got {type(data).__name__}")

async def send_message(self, data: dict):
    try:
        await self.__wbs.send(str(dict(data)))
    except ValueError:
        raise ValueError(f"\"data\" parameter expects a dictionary or a dictionary convertable object. Got {type(data).__name__}")

websockets.WebSocketClientProtocol.send_message = send_message