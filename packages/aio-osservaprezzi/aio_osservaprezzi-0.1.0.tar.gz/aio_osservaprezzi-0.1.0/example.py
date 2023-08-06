import aiohttp
import asyncio
from aio_osservaprezzi import (
    OsservaPrezzi,
    StationsNotFoundException,
    RegionNotFoundException,
)

loop = asyncio.get_event_loop()

SAMPLE = {"town": "Santa Maria Imbaro", "region": "Abruzzo", "province": "CH"}


async def test():
    async with aiohttp.ClientSession() as session:
        api = OsservaPrezzi(session, parameters=SAMPLE,)

        try:
            data_by_id = await api.get_station_by_id(47715)
            print(data_by_id)
        except (StationsNotFoundException or RegionNotFoundException) as e:
            print(e)


loop.run_until_complete(test())
loop.close()
