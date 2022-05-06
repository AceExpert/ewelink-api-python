from typing import Iterable

from .enumerations import DeviceType, DeviceChannelLengh, Power, CountryCodes, Region
from .user import AppInfo, ClientInfo, ClientUser
from .device import Device, Network, Pulse
from .asset import Asset
from .object import Object

PowerState = Power

class Devices(list[Device]):
    def __init__(self, devices: Iterable[Device]):
        super().__init__(devices)

    def get(self, id: str) -> Device | None:
        for device in self:
            if device.id == id: return device

del Iterable