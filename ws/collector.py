import typing, datetime, asyncio

class EventCollector:
    def __init__(self, websocket, time: float) -> None:
        self.__websocket = websocket
        self.__time = time
    async def collect(self, event: str, check: typing.Callable = None) -> typing.List[typing.Any]:
        collected = []
        start_time = datetime.datetime.utcnow()
        while (datetime.datetime.utcnow() - start_time).total_seconds() < self.__time:
            try:
                event_data = await self.__websocket.wait_for(event, 
                                                             check=check, 
                                                             timeout=self.__time - (datetime.datetime.utcnow()-start_time).total_seconds())                
                collected.append(event_data)
            except asyncio.TimeoutError:
                pass
        return collected