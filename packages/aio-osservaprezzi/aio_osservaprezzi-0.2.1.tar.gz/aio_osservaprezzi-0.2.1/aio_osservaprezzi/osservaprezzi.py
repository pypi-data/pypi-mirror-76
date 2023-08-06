"""OsservaPrezzi class for aio_osservaprezzi."""

from .const import ENDPOINT, REGIONS
from .models import Station
from .exceptions import (
    RegionNotFoundException,
    StationsNotFoundException,
    OsservaPrezziConnectionError,
    OsservaPrezziException,
)
from typing import Any
import asyncio
import aiohttp
import async_timeout


class OsservaPrezzi:
    def __init__(
        self,
        parameters,
        session: aiohttp.ClientSession = None,
        request_timeout: int = 8,
    ) -> "OsservaPrezzi":
        """Initialize connection with OsservaPrezzi API."""
        self._session = session
        self._close_session = False
        self.request_timeout = request_timeout

        try:
            self._parameters = f"region={REGIONS[parameters['region']]}\
                                &province={parameters['province']}\
                                &town={parameters['town']}\
                                &carb="
        except KeyError as exception:
            raise RegionNotFoundException(
                "Error occurred while trying to find the region."
            ) from exception

    async def _request(self) -> Any:
        """Handle a request to OsservaPrezzi API."""
        method = "POST"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method, ENDPOINT, data=self._parameters, headers=headers,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise OsservaPrezziConnectionError(
                "Timeout occurred while connecting to OsservaPrezzi."
            ) from exception
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as exception:
            raise OsservaPrezziConnectionError(
                "Error occurred while connecting to OsservaPrezzi."
            ) from exception

        if "application/json" not in response.headers.get("Content-Type", ""):
            raise OsservaPrezziException("Unexpected response from OsservaPrezzi.")

        return (await response.json())["array"]

    async def get_stations(self):
        data = await self._request()
        try:
            return [Station.from_dict(s) for s in data]
        except Exception:
            raise StationsNotFoundException("Couldn't find stations.")

    async def get_station_by_id(self, id):
        stations = await self.get_stations()
        try:
            return next(filter(lambda d: d.id == id, stations))
        except Exception:
            raise StationsNotFoundException("Couldn't find specified station.")

    async def close(self):
        """Close the session."""
        if self._close_session and self._session:
            await self._session.close()

    async def __aenter__(self) -> "OsservaPrezzi":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
