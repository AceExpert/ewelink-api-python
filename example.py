import ewelink
from ewelink import Client

@ewelink.login('password', 'user@email.com')
async def main(client: Client):
    print(client.region)
    print(client.user.info)