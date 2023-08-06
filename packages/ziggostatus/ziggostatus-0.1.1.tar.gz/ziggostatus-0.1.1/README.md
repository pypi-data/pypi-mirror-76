## Python API fetching Ziggo outages & announcements

Use this package to check with the VodafoneZiggo API for outages & announcements on a VodafoneZiggo address.

![Test ziggostatus package](https://github.com/DevSecNinja/ZiggoStatus/workflows/Test%20ziggostatus%20package/badge.svg?branch=master)

## Usage

```` python
import asyncio
import aiohttp

from ziggostatus import get_ziggo_status

postalcode = "1012JS" # Amsterdam - Dam Square
housenumber = "1"

async def main():
    session = aiohttp.ClientSession()
    status = await get_ziggo_status(postalcode, housenumber, session)
    print(f"{status}")

    await session.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
````
