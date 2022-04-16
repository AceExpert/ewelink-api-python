import aiohttp, time, random, asyncio

from .models import ClientUser, Devices
from .constants import Constants as constants
from .http import HttpClient
from .utils import nonce

class WebSocketClient:
    http: HttpClient
    heartbeat: int
    ws: aiohttp.ClientWebSocketResponse | None
    session: aiohttp.ClientSession
    user: ClientUser
    devices: Devices
    ping_task: asyncio.Task[None] | None

    def __init__(self, http: HttpClient, user: ClientUser, devices: Devices = Devices([])) -> None:
        self.http = http
        self.user = user
        self.devices = devices
        self.heartbeat = 90
        self.ping_task = None
        self.session = http.session
        self.ws = None

    def set_devices(self, devices: Devices):
        self.devices = devices

    async def create_websocket(self, domain: str, port: int | str):
        self.ws = await self.session.ws_connect(f'wss://{domain}:{port}/api/ws')
        await self.ws.send_json({
            "action": "userOnline",
            "version": 8,
            "ts": int(time.time()),
            "at": self.http.token,
            "userAgent": "app",
            "apikey": self.user.api_key,
            "appid": constants.APP_ID,
            "nonce": "".join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(8)),
            "sequence": str(time.time() * 1000)
        })
        response: dict[str, str | int | dict[str, int]] = await self.ws.receive_json()
        if not response.get('error'):
            if config := response.get('config', {}):
                if type(config) == dict:
                    if hb_interval := response['config'].get('hbInterval', ''):
                        if type(hb_interval) == int: self.heartbeat = hb_interval + 7
        self.ping_task = self.http.loop.create_task(self.ping_hb())

    async def ping_hb(self):
        while True:
            await asyncio.sleep(self.heartbeat)
            await self.ws.send_str("ping")

    async def close(self):
        await self.ws.close()

    @property
    def closed(self) -> bool:
        return self.ws.closed