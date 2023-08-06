import asyncio

import aiohttp
import pytest
from aio_osservaprezzi import (
    OsservaPrezzi,
    OsservaPrezziConnectionError,
)
from aio_osservaprezzi.const import ENDPOINT

SAMPLE = {"town": "Lanciano", "region": "Abruzzo", "province": "CH"}


@pytest.mark.asyncio
async def test_unexpected_response(aresponses):
    aresponses.add(
        ENDPOINT, "post", aresponses.Response(text="SHIT", status=200),
    )

    async with aiohttp.ClientSession() as session:
        api = OsservaPrezzi(session, {})
        with pytest.raises(Exception):
            assert await api._request()


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from the Elgato Key Light."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(2)
        return aresponses.Response(body="Goodmorning!")

    aresponses.add(ENDPOINT, "post", response_handler)

    async with aiohttp.ClientSession() as session:
        api = OsservaPrezzi(SAMPLE, session, 1)
        with pytest.raises(OsservaPrezziConnectionError):
            assert await api._request()
