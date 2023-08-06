import asyncio

import aiohttp
import pytest
from aio_osservaprezzi import (
    OsservaPrezzi,
    StationsNotFoundException,
    OsservaPrezziConnectionError,
    OsservaPrezziException,
)

from . import load_fixture

SAMPLE = {"town": "Lanciano", "region": "Abruzzo", "province": "CH"}


@pytest.mark.asyncio
async def test_json_request(aresponses):
    """Test JSON response handling."""
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
        response = await osservaprezzi._request()
        assert response


@pytest.mark.asyncio
async def test_internal_aiohttp_session(aresponses):
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

    async with OsservaPrezzi(SAMPLE) as osservaprezzi:
        response = await osservaprezzi._request()
        assert response


@pytest.mark.asyncio
async def test_timeout(aresponses):
    async def response_handler(_):
        await asyncio.sleep(2)
        return aresponses.Response(body="Not important.")

    aresponses.add(
        "carburanti.mise.gov.it",
        "/OssPrezziSearch/ricerca/localita",
        "POST",
        response_handler,
    )

    async with aiohttp.ClientSession() as session:
        osservaprezzi = OsservaPrezzi(SAMPLE, session=session, request_timeout=1)
        with pytest.raises(OsservaPrezziConnectionError):
            assert await osservaprezzi._request()


@pytest.mark.asyncio
async def test_unexpected_response(aresponses):
    aresponses.add(
        "carburanti.mise.gov.it",
        "/OssPrezziSearch/ricerca/localita",
        "POST",
        aresponses.Response(status=200, text="Unexpected",),
    )

    async with aiohttp.ClientSession() as session:
        osservaprezzi = OsservaPrezzi(SAMPLE, session)
        with pytest.raises(OsservaPrezziException):
            assert await osservaprezzi._request()


@pytest.mark.asyncio
async def test_http_error_404(aresponses):
    aresponses.add(
        "carburanti.mise.gov.it",
        "/OssPrezziSearch/ricerca/localita",
        "POST",
        aresponses.Response(status=404, text="Unexpected",),
    )

    async with aiohttp.ClientSession() as session:
        osservaprezzi = OsservaPrezzi(SAMPLE, session)
        with pytest.raises(OsservaPrezziException):
            assert await osservaprezzi._request()


@pytest.mark.asyncio
async def test_station_not_found(aresponses):
    aresponses.add(
        "carburanti.mise.gov.it",
        "/OssPrezziSearch/ricerca/localita",
        "POST",
        aresponses.Response(
            status=200,
            text='{"array": []}',
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        osservaprezzi = OsservaPrezzi(SAMPLE, session)
        with pytest.raises(StationsNotFoundException):
            assert await osservaprezzi.get_station_by_id(123)


@pytest.mark.asyncio
async def test_empty_stations_not_found(aresponses):
    aresponses.add(
        "carburanti.mise.gov.it",
        "/OssPrezziSearch/ricerca/localita",
        "POST",
        aresponses.Response(
            status=200,
            text='{"array": []}',
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        osservaprezzi = OsservaPrezzi(SAMPLE, session)
        assert len(await osservaprezzi.get_stations()) == 0
