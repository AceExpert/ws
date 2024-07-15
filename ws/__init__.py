from typing import Literal, NamedTuple

from .client import ClientSocket
from .server import ServerSocket
from .models import Message, Object
from .wsprotocols import WSSProtocol, WSCProtocol
from .exceptions import ParameterConflict, EventNotFound
from .collector import EventCollector

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int

__version__: str = "2.1.3"
__author__: str = "Cybertron"
version_info: VersionInfo = VersionInfo(major=2, minor=1, micro=3, releaselevel='final', serial=0)
__copyright__: str = "Copyright (c) 2021 - present Cybertron"