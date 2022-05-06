from typing import Any
from datetime import datetime
from dataclasses import dataclass

from .enumerations import CountryCodes, Region
from .object import Object
from ..http import HttpClient

@dataclass
class AppInfo:
    os: str | None
    version: str | None

@dataclass
class ClientInfo:
    version: str | None
    imei: str | None
    model: str | None
    os: str | None
    rom_version: str | int | None

class ClientUser:
    ip_country: str | None
    online_time: datetime | None
    offline_time: datetime | None
    location: str | None
    http: HttpClient | None
    app_infos: list[AppInfo]
    info: ClientInfo

    def __init__(self, data: dict[str, str | bool | dict[str, str | bool | int | Any]], http: HttpClient | None) -> None:
        self.email: str | None = data.get('email', None)
        self.region: Region = Region[http.region.upper()]
        self.ip_country = None
        self.location = None
        self.language: str = data.get('language', data.get('lang', 'en'))
        self.phone_number: str | None = data.get('phoneNumber', None)
        self.api_key: str = data.get('apikey')
        self.id: str = data['_id']
        self.country_code: CountryCodes | None =\
            CountryCodes.__dict__['_value2member_map_'].get(
                data.get('countryCode', "0"), "0"
            )
        self.online_time = None
        self.offline_time = None
        self.created_at: datetime = datetime.strptime(data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.family_id: str | None = data.get('currentFamilyId', None)
        if extra := data.get('extra', None):
            if ip := extra.get('ipCountry', None):
                self.ip_country: str = ip
        if online_time := data.get('onlineTime', None):
            self.online_time: datetime = datetime.strptime(online_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if offline_time := data.get('offlineTime', None):
            self.offline_time: datetime = datetime.strptime(offline_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.online: bool = data.get('online', False)
        if location := data.get('location', None):
            self.location = location
        self.http = http
        self.app_infos: list[AppInfo] = [AppInfo(os=info['os'] if info.get('os', None) else None, 
                                                 version=info['appVersion'] if info.get('appVersion', None) else None) 
                                         for info in data.get('appInfos', [])]
        self.info: ClientInfo = ClientInfo(
            version=data['clientInfo']['appVersion'] if data['clientInfo'].get('appVersion', None) else None,
            imei=data['clientInfo']['imei'] if data['clientInfo'].get('imei', None) else None,
            model = data['clientInfo']['model'] if data['clientInfo'].get('model', None) else None,
            os = data['clientInfo']['os'] if data['clientInfo'].get('os', None) else None,
            rom_version = data['clientInfo']['romVersion'] if data['clientInfo'].get('romVersion', None) else None,
        )
        self.data: Object = Object(data, name = 'UserData')
        