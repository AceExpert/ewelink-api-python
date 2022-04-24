# ewelink-api-python
An API Wrapper for the Ewelink platform.
The API Documentation can be found [here](https://coolkit-technologies.github.io/eWeLink-API/#/en).

## Python
Python 3.10+

## Example
```py
import ewelink
from ewelink import Client, PowerState, DeviceOffline

@ewelink.login('password', 'user.name@email.com')
async def main(client: Client):
    print(client.region)
    print(client.user.info)
    print(client.devices)
    
    device = client.devices.get('10008ecfd9')
    
    print(device.state)
    print(device.created_at)
    print("Brand Name:", device.brand.name, "Logo URL:", device.brand.logo.url)
    print("Device online?", device.online)
    
    try:
        await device.edit(PowerState.on)
    except DeviceOffline:
        print("Device is offline!")
```

Other HTTP methods will be added later.
