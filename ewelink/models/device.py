from typing import Any, Callable, Coroutine
from datetime import datetime
from dataclasses import dataclass

from .asset import Asset
from .object import Object
from .enumerations import Power, DeviceType
from ..state import Connection
from ..exceptions import DeviceOffline
from ..utils import generics
from ..customtypes import Subscriptable

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
    _state: Connection | None = None
    online_time: datetime | None
    offline_time: datetime | None

    def __init__(self, data: dict[str, str | int | Any], state: Connection | None) -> None:
        self.apikey: str | None = data.get('apikey', None)
        self.id: str = data.get('deviceid', '0')
        self.brand: Brand = Brand(
            name = data.get('brandName', None), 
            logo = Asset(data.get('brandLogoUrl', None), session=state.http.session if state else None)
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
        self.params: Object = Object(data['params'], name = "Params")
        self.state: Power = Power[data['params']['switches'][0]['switch']] if data['params'].get("switches", None) else Power.unknown
        self.startup: Power = Power[data['params']['startup']] if data['params'].get('startup', None) else Power.unknown
        self.pulse: Pulse = Pulse(
            state=Power[data['params']['pulse']] if data['params'].get('pulse', None) else Power.unknown,
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
        self._state = state
        self.type: DeviceType = DeviceType.__dict__['_value2member_map_'].get(int(data.get('type', 0), 16), 0)

    async def edit(self, *states: Power, startup: Power = None, pulse: Pulse | Power = None, pulse_width: int = None):
        try:
            _switch: dict[str, list[dict[str, str | int]] | str | int] = {}
            for state in states:
                _state = state.to_dict()
                if 'switches' in _switch:
                    if 'switches' not in _state:
                        raise TypeError('The argument to states must either be single channel device command (eg: Power.on, Power.off) or atmost two multi-channel device command (eg: (Power.on[0, 1], Power.off[2, 3]) , Power.off[2, 3, 4]).')
                    _switch['switches'].append(_state['switches'])
                else:
                    _switch.update(_state)
            params = dict(
                startup = startup.name if startup else self.startup.name,
                pulse = pulse.name if isinstance(pulse, Power) else pulse.state.name if pulse else self.pulse.state.name,
                pulseWidth = pulse_width or self.pulse.width
            )
            params.update(_switch)
            await self._state.ws.update_device_status(self.id, **params)
        except DeviceOffline as offline:
            raise DeviceOffline(*offline.args) from offline
        else:
            self.state = (state or self.state) if _switch.get('switch', None) else self.state
            self.startup = startup or self.startup
            if isinstance(pulse, Pulse):
                self.pulse = pulse
            elif isinstance(pulse, Power):
                self.pulse.state = pulse
            self.pulse.width = pulse_width or self.pulse.width
            if switches := _switch.get('switches', None):
                if 'switches' in self.params:
                    self.params.switches = switches

    @property
    def on(self) -> Subscriptable[int, Callable[[], Coroutine[None, Any, None]]]:
        return self._on(self)

    @property
    def off(self) -> Subscriptable[int, Callable[[], Coroutine[None, Any, None]]]:
        return self._off(self)

    @property
    def switches(self) -> Subscriptable[int, Callable[[Power], Coroutine[None, Any, None]]]:
        return self._switches(self)

    @generics(int, ...)
    def _on(self, types = tuple()):
        return self.edit(Power.on[types] if types else Power.on)

    @generics(int, ...)
    def _off(self, types = tuple()):
        return self.edit(Power.off[types] if types else Power.off)

    @generics(int, ...)
    def _switches(self, state: Power, types = tuple()):
        return self.edit(state[types] if types else state)

    def __repr__(self) -> str:
        return f"<Device name={self.name} id={self.id} switch={self.state} online?={self.online} type={self.type} network={self.network}>"

    def __str__(self) -> str:
        return self.id