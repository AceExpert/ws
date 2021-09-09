from .client import ClientSocket
from .server import ServerSocket
from .models import Message, Object
from .wsprotocols import WSSProtocol, WSCProtocol
from .exceptions import ParameterConflict, EventNotFound
from .collector import EventCollector

__version__ = "2.1.0"
__author__ = "Cybertron"
