from .client import ClientSocket
from .server import ServerSocket
from .models import Message, Object
from .wsprotocols import WSSProtocol, WSCProtocol
from .exceptions import ParameterConflict
from .collector import EventCollector

__version__ = "2.0.0"
__author__ = "Cybertron"
