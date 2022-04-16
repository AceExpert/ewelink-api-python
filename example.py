import ewelink
from ewelink import Client

@ewelink.login('password', 'user.name@email.com')
async def main(client: Client):
    print(client.region)
    print(client.user.info)
    print(client.devices)
    
    device = client.devices.get('10008ecfd9')
    
    print(device.state)
    print(device.created_at)
    print("Brand Name:", device.brand.name, "Logo URL:", device.brand.logo.url)
    print("Device online?", device.is_online)