# ewelink-api-python
An API Wrapper for the Ewelink platform.
The API Documentation can be found [here](https://coolkit-technologies.github.io/eWeLink-API/#/en).

## Python
Python 3.9+

## Example
```py
import ewelink
from ewelink import Client

@ewelink.login('password', 'user@email.com')
async def main(client: Client):
    print(client.region)
    print(client.user.info)
```

Other HTTP methods will be added later.
