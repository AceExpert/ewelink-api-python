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

from .exceptions import *
from .http import HttpClient

T = TypeVar("T")
V = TypeVar("V")

Decorator = Callable[[Callable[[T], Coroutine[None, Any, V]]], V]

class Client:
    from .models import ClientUser
    
    http: HttpClient
    user: ClientUser | None
    loop: asyncio.AbstractEventLoop

    def __init__(self, password: str, email: str | None = None, phone: str | int | None = None, *, region: str = 'us'):
        super().__init__()
        self.http = HttpClient(password = password, email = email, phone = phone, region = region)
        self.user = None

    async def setup(self):
        self.loop = asyncio.get_event_loop()
        await self.http._create_session(loop=self.loop)
        self.user = await self.http.login()

    @property
    def region(self):
        return self.http.region

    @classmethod
    def login(cls: Type[T], password: str, email: str | None = None, phone: str | int | None = None, *, region: str = 'us') -> Decorator[T, V]:
        client: Client = cls(password, email, phone, region = region)
        asyncio.get_event_loop().run_until_complete(client.setup())
        def decorator(f: Callable[[Client], Coroutine[None, Any, V]]) -> V:
            result = asyncio.get_event_loop().run_until_complete(f(client))
            asyncio.get_event_loop().run_until_complete(client.http.session.close())
            return result
        return decorator

def login(password: str, email: str | None = None, phone: str | int | None = None, *, region: str = 'us') -> Decorator[Client, V]:
        client: Client = Client(password, email, phone, region = region)
        asyncio.get_event_loop().run_until_complete(client.setup())
        def decorator(f: Callable[[Client], Coroutine[None, Any, V]]) -> V:
            result = asyncio.get_event_loop().run_until_complete(f(client))
            asyncio.get_event_loop().run_until_complete(client.http.session.close())
            return result
        return decorator