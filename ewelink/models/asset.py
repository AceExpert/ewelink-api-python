import re, os
from aiohttp import ClientSession

class Asset:
    url: str
    hash: str
    session: ClientSession | None
    
    def __init__(self, url: str = None, hash: str = None, session: ClientSession = None) -> None:
        if url and re.match(r"(?:^(?:https|http)://[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+)|(?:<a?\:[a-zA-Z0-9_]+:[0-9]+>)", url, flags=re.I):
            self.url = url
            if img_hash := re.findall(r'^.+/(\w+)(?:\W|\s).*$', url, flags=re.IGNORECASE):
                self.hash = img_hash[0]
        elif hash:
            self.url = f'https://as-ota.coolkit.cc/logo/{hash}.png'
            self.hash = hash
        self.session = session

    async def read(self) -> str:
        if self.session:
            resp = await self.session.get(self.url)
            if resp.status == 200:
                return await resp.text()
        
        return str()

    async def save(self, filename: str = 'logo.png', path: str = None) -> int | None:
        path = path if path else os.getcwd()
        with open(path.strip(f"/{filename.strip('/')}"), 'w') as file: 
            return file.write(await self.read())