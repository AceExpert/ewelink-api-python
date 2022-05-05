import aiohttp,\
       asyncio,\
       time,\
       uuid,\
       re

import base64, hmac, json, hashlib

from typing import TypedDict, Any

from .constants import Constants as constants
from .utils import nonce

CredentialsDict = TypedDict(
    'CredentialsDict', 
    {
        'appid': str,
        'password': str,
        'ts': int,
        'version': int,
        'nonce': str,
        'os': str,
        'model': str,
        'romVersion': str,
        'appVersion': str,
        'imei': str,
        'email': str | None,
        'phoneNumber': str | None
    }
)

class HttpClient:
    region: str 
    email: str | None
    phone: str | None
    password: str
    token: str | None
    refresh_token: str | None
    credentials: CredentialsDict | None
    sign: str | None
    loop: asyncio.AbstractEventLoop | None
    session: aiohttp.ClientSession | None
    BASE: str
    
    __slots__ = ('region', 'session', 'loop', 'password', 'email', 'phone', 'sign', 'credentials', 'BASE', 'token', 'refresh_token')
    def __init__(self, password: str, email: str | None = None, phone: str | int | None = None, region: str = 'us') -> None:
        self.session = None
        self.password = password
        self.credentials = None
        self.region = region
        self.loop = None
        self.sign = None
        self.token = None
        self.refresh_token = None
        self.BASE = f"https://{region}-api.coolkit.cc:8080/api"
        self.email = email
        self.phone = phone

    async def _create_session(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()

    async def login(self, **kwargs: CredentialsDict | str | None) -> dict[str, str | bool | dict[str, str | bool | int | Any]]:
        self.credentials = kwargs.get('credentials', None) or\
        {
            'appid': constants.APP_ID,
            'password': self.password,
            'ts': int(time.time()),
            'version': 6,
            'nonce': nonce(),
            'os': 'iOS',
            'model': 'iPhone10,6',
            'romVersion': '11.1.2',
            'appVersion': '3.5.3',
            'imei': str(uuid.uuid4())
        } 
        if (
           not self.email 
           or not re.match(r'^[a-zA-Z0-9.]+@[a-zA-Z\-]+\.[a-zA-Z]+(?:(?:\.[a-zA-Z]+)+?)?$', self.email, re.I) 
           and re.match(r'^(?:\+?\d{,4})?\d{10}$', str(self.phone).replace(' ', '').replace('(', '').replace(')', ''))
        ):
            self.credentials['phoneNumber'] = self.phone
        else:
            self.credentials['email'] = self.email
        self.sign = kwargs.get('sign', None) or base64.b64encode(
            hmac.new(constants.APP_SECRET, msg=json.dumps(self.credentials).encode(), digestmod=hashlib.sha256).digest()
        ).decode()
        response = await self.session.post(self.BASE+'/user/login', headers = { "Authorization": f'Sign {self.sign}'}, json = self.credentials)
        data: dict[str, Any] = await response.json()
        if 'error' in data:
            if region := data.get('region', None):
                self.region = region
                self.BASE = f"https://{region}-api.coolkit.cc:8080/api"
                return await self.login(credentials = self.credentials, sign = self.sign)
            else:
                print(data)
        else:
            self.token = data.get('at')
            self.refresh_token = data.get('rt')
            return data.get('user', {'_id': '0', 'clientInfo': {}, 'createdAt': '1000-01-01T00:00:00.000Z'})
    
    async def get_devices(self) -> dict[str, list[dict[str, str | int | Any]]]:
        response =\
        await self.session.get(self.BASE + '/user/device', 
            params=\
            {
                'lang': 'en',
                'appid': constants.APP_ID,
                'ts': int(time.time()),
                'version': 8,
                'getTags': 1,
            }, 
            headers = {'Authorization': f'Bearer {self.token}'})
        return await response.json()

    async def get_gateway(self) -> dict[str, Any]:
        response = await self.session.get(
            f'https://{self.region}-dispa.coolkit.cc/dispatch/app', 
            headers = {
                'Authorization': f'Token {self.token}'
            }
        )
        return await response.json()