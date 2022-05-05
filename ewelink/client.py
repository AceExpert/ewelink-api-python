import aiohttp ,\
       base64, \
       hashlib,\
       hmac,\
       time,\
       random,\
       json,\
       uuid,\
       re,\
       asyncio

from typing import TypeVar, Type, Callable, Coroutine, Any
from dataclasses import dataclass

from .models import ClientUser, Device, Devices, Region
from .http import HttpClient
from .ws import WebSocketClient
from .state import Connection

T = TypeVar("T")
V = TypeVar("V")
ClientT = TypeVar("ClientT", bound="Client")
GatewayT = TypeVar("GatewayT", bound="Gateway")

Decorator = Callable[[Callable[[T], Coroutine[None, Any, V]]], V]

@dataclass
class Gateway:
    domain: str
    port: int | str

    @classmethod
    def from_dict(cls: Type[GatewayT], data: dict[str, str | int]) -> GatewayT:
        return cls(domain = data.get("domain"), port = data.get("port"))

class Client:
    http: HttpClient
    gateway: Gateway | None = None
    ws: WebSocketClient | None
    _devices: dict[str, Device] = {}
    user: ClientUser | None
    loop: asyncio.AbstractEventLoop

    def __init__(self, password: str, email: str | None = None, phone: str | int | None = None, *, region: str = 'us'):
        super().__init__()
        self.http = HttpClient(password = password, email = email, phone = phone, region = region)
        self.ws = None
        self.user = None

    async def login(self):
        self.loop = asyncio.get_event_loop()
        await self.http._create_session(loop=self.loop)
        self.user = ClientUser(data = await self.http.login(), http=self.http)
        self.ws = WebSocketClient(http = self.http, user = self.user)
        self.gateway = Gateway.from_dict(await self.http.get_gateway())
        await self.ws.create_websocket(self.gateway.domain, self.gateway.port)
        self._devices =\
        {
            device['deviceid']: Device(data = device, state = self._get_state()) for device in (await self.http.get_devices()).get('devicelist', [])
        }
        self.ws.set_devices(self._devices)

    def _get_state(self) -> Connection:
        return Connection(ws = self.ws, http = self.http)

    def get_device(self, id: str) -> Device | None:
        return self.devices.get(id)

    @property
    def devices(self):
        return Devices(self._devices.values())

    @property
    def region(self):
        return Region[self.http.region.upper()]

    @classmethod
    def setup(cls: Type[ClientT], password: str, email: str | None = None, phone: str | int | None = None, *, region: str = 'us') -> Decorator[ClientT, V]:
        client: Client = cls(password, email, phone, region = region)
        def decorator(f: Callable[[Client], Coroutine[None, Any, V]]) -> V:
            result = asyncio.get_event_loop().run_until_complete(f(client))
            if not client.http.session.closed:
                asyncio.get_event_loop().run_until_complete(client.http.session.close())
            if client.ws:
                if not client.ws.closed:
                    asyncio.get_event_loop().run_until_complete(client.ws.close())
            return result
        return decorator

def login(password: str, email: str | None = None, phone: str | int | None = None, *, region: str = 'us') -> Decorator[Client, V]:
        client: Client = Client(password, email, phone, region = region)
        asyncio.get_event_loop().run_until_complete(client.login())
        def decorator(f: Callable[[Client], Coroutine[None, Any, V]]) -> V:
            result = asyncio.get_event_loop().run_until_complete(f(client))
            if not client.http.session.closed:
                asyncio.get_event_loop().run_until_complete(client.http.session.close())
            if client.ws:
                if not client.ws.closed:
                    asyncio.get_event_loop().run_until_complete(client.ws.close())
            return result
        return decorator