import aiohttp
import pytest

from aio_osservaprezzi import OsservaPrezzi, Fuel

from . import load_fixture

SAMPLE = {"town": "Lanciano", "region": "Abruzzo", "province": "CH"}


@pytest.mark.asyncio
async def test_station(aresponses):
    """Test getting station information."""
    aresponses.add(
        "carburanti.mise.gov.it",
        "/OssPrezziSearch/ricerca/localita",
        "POST",
        aresponses.Response(
            status=200,
            text=load_fixture("response.json"),
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        osservaprezzi = OsservaPrezzi(SAMPLE, session)
        fuel: Fuel = (await osservaprezzi.get_station_by_id(12345)).fuels[0]
        assert fuel
        assert fuel.name == "Carb1"
        assert fuel.id == 1
        assert not fuel.is_self
        assert fuel.price == "1,234"
