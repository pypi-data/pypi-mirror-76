## Python API fetching Ziggo F1 broadcasts

Use this package to get Formula 1 broadcasts from Ziggo.

![Test ziggof1broadcasts package](https://github.com/DevSecNinja/ZiggoF1Broadcasts/workflows/Test%20ziggof1broadcasts%20package/badge.svg?branch=master)

## Usage

```` python
import aiohttp
import asyncio

from datetime import date
from ziggof1broadcasts import get_ziggo_f1_broadcasts

async def main():
    session = aiohttp.ClientSession()

    # By default, it will return the broadcasts of today, but you can provide a date
    startTime = date.fromisoformat('2020-08-16')

    broadcasts = await get_ziggo_f1_broadcasts(session, startTime=startTime)
    print(f"{broadcasts}")

    await session.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

````
