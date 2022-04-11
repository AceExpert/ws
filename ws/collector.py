from datetime import datetime
from typing import Callable, List, Any
from asyncio import TimeoutError

class EventCollector:
    __slots__ = '__websocket', '__time'
    
    def __init__(self, websocket, time: float) -> None:
        self.__websocket = websocket
        self.__time = time
    async def collect(self, event: str, check: Callable = None) -> List[Any]:
        collected = []
        start_time = datetime.datetime.utcnow()
        while (datetime.utcnow() - start_time).total_seconds() < self.__time:
            try:
                event_data = await self.__websocket.wait_for(event, 
                                                             check=check, 
                                                             timeout=self.__time - (datetime.datetime.utcnow()-start_time).total_seconds())                
                collected.append(event_data)
            except TimeoutError:
                pass
        return collected
