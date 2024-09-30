from typing import ClassVar

class Constants:
    APP_ID: ClassVar[str] = 'R8Oq3y0eSZSYdKccHlrQzT1ACCOUT9Gv'
    APP_SECRET: ClassVar[bytes] = b'1ve5Qk9GXfUhKAn1svnKwpAlxXkMarru'
    errors: ClassVar[dict[int, str]] =\
    {
        400: 'Parameter error',
        401: 'Wrong account or password',
        402: 'Email inactivated',
        403: 'Forbidden',
        404: 'Device does not exist',
        406: 'Authentication failed',
        503: 'Service Temporarily Unavailable or Device is offline'
    }
    customErrors: ClassVar[dict[str, str]] =\
    {
        'ch404': 'Device channel does not exist',
        'unknown': 'An unknown error occurred',
        'noDevices': 'No devices found',
        'noPower': "No power usage data found",
        'noSensor': 'Can\'t read sensor data from device',
        'noFirmware': "Can't get model or firmware version",
        'invalidAuth': 'Library needs to be initialized using email and password',
        'invalidCredentials': 'Invalid credentials provided',
        'invalidPower': 'Invalid power state. Expecting: "on", "off" or "toggle"',
    }