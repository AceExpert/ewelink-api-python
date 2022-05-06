# ewelink-api-python
An API Wrapper for the Ewelink platform.
The API Documentation can be found [here](https://coolkit-technologies.github.io/eWeLink-API/#/en).

## Python
Python 3.10+

## Example
```py
import ewelink
from ewelink import Client, DeviceOffline

@ewelink.login('password', 'user.address@email.com')
async def main(client: Client):
    print(client.region)
    print(client.user.info)
    print(client.devices)
    
    device = client.get_device('10008ecfd9')
    
    print(device.params) 
        #Raw device specific properties 
        #can be accessed easily like: device.params.switch or device.params['startup'] (a subclass of dict)

    print(device.state)
    print(device.created_at)
    print("Brand Name:", device.brand.name, "Logo URL:", device.brand.logo.url)
    print("Device online?", device.online)
    
    try:
        await device.on()
    except DeviceOffline:
        print("Device is offline!")
```

Other HTTP methods will be added later.
