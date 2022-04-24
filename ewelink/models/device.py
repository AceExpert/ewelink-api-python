from typing import Any
from datetime import datetime
from dataclasses import dataclass

from .asset import Asset
from .enumerations import Power, DeviceType
from ..http import HttpClient
from ..ws import WebSocketClient

@dataclass
class Brand:
    name: str | None
    logo: Asset

@dataclass
class Network:
    ssid: str | None
    sta_mac: str | None

@dataclass
class Pulse:
    state: Power
    width: int

class Device:
    ws: WebSocketClient | None
    http: HttpClient | None
    online_time: datetime | None
    offline_time: datetime | None

    def __init__(self, data: dict[str, str | int | Any], http: HttpClient | None = None, ws: WebSocketClient | None = None) -> None:
        self.apikey: str | None = data.get('apikey', None)
        self.id: str = data.get('deviceid', '0')
        self.brand: Brand = Brand(
            name = data.get('brandName', None), 
            logo = Asset(data.get('brandLogoUrl', None), session=http.session if http else None)
        )
        self.url: str | None = data.get('deviceUrl', None)
        self.hash_id: str = data.get('_id', '0')
        self.created_at: datetime = datetime.strptime(data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.key: str = data.get('devicekey', '0')
        self.name: str | None = data.get('name', None)
        self.online_time = None
        self.offline_time = None
        if online_time := data.get('onlineTime', None):
            self.online_time = datetime.strptime(online_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if offline_time := data.get('offlineTime', None):
            self.offline_time = datetime.strptime(offline_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.state: Power = Power[data['params']['switch']]
        self.startup: Power = Power[data['params']['startup']] if data['params'].get('startup', None) else Power.off
        self.pulse: Pulse = Pulse(
            state=Power[data['params']['pulse']] if data['params'].get('pulse', None) else Power.off,
            width=data['params'].get('pulseWidth', 0)
        )
        self.network: Network = Network(
            ssid = data['params'].get('ssid', None),
            sta_mac = data['params'].get('staMac', None)
        )
        self.version: int = data['params'].get('version', 0)
        self.online: bool = data.get('online', False)
        self.location: str | None = data.get('location') if data.get('location', None) else None
        self.data = data
        self.ws = ws
        self.http = http
        self.type: DeviceType = DeviceType.__dict__['_value2member_map_'].get(int(data.get('type', 0)), 0)

    async def edit(self, state: Power = None, startup: Power = None, pulse: Pulse | Power = None, pulse_width: int = None):
        await self.ws.update_device_status(self.id,
            switch = state.name if state else self.state.name,
            startup = startup.name if startup else self.startup.name,
            pulse = pulse.name if isinstance(pulse, Power) else pulse.state.name if pulse else self.pulse.state.name,
            pulseWidth = pulse_width or self.pulse.width
        )

    def __repr__(self) -> str:
        return f"<Device name={self.name} id={self.id} switch={self.state} online?={self.online} type={self.type} network={self.network}>"

    def __str__(self) -> str:
        return self.id