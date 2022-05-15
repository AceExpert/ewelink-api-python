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
    
    device = client.get_device('10008ecfd9') #single channel device
    device2 = client.get_device('10007fgah9') #four channel device
    
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
### Multi channel device control (First method)
```py
    try:
        await device2.on[0, 2]() #turns on 1st and 3rd channel
        await device2.off[1, 3]() #turns off 2nd and 4th channel
    except DeviceOffline:
        print("Device is offline!")
```
### Multi channel device control (Second method)
```py
    try:
        await device2.edit(Power.on[0, 2]) #turns on 1st and 3rd channel
        await device2.edit(Power.off[1, 3]) #turns off 2nd and 4th channel
    except DeviceOffline:
        print("Device is offline!")
```

Other HTTP methods will be added later.
