## Python API fetching Ziggo outages & announcements

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