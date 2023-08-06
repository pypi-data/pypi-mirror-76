import aiohttp
import pytest

from aio_osservaprezzi import OsservaPrezzi, Station

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
        station: Station = await osservaprezzi.get_station_by_id(12345)
        assert station
        assert station.name == "Test"
        assert station.latitude == "1"
        assert station.longitude == "2"
        assert station.id == 12345
        assert station.bnd == "AGIP"
        assert station.addr == "ADDR"
        assert station.update == "2020-02-02 12:12"
