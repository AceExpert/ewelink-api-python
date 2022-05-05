from dataclasses import dataclass

@dataclass
class Connection:
    from .http import HttpClient
    from .ws import WebSocketClient

    ws: WebSocketClient
    http: HttpClient