from dataclasses import dataclass
from .http import HttpClient
from .ws import WebSocketClient

@dataclass
class Connection:
    ws: WebSocketClient
    http: HttpClient