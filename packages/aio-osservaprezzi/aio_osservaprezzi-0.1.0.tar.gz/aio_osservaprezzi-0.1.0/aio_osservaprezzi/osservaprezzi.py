"""OsservaPrezzi class for aio_osservaprezzi."""

from .const import ENDPOINT, REGIONS
from .models import Station
from .exceptions import (
    RegionNotFoundException,
    StationsNotFoundException,
    OsservaPrezziConnectionError,
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
    ) -> None:
        """Initialize connection with OsservaPrezzi API."""
        self._session = session
        self._parameters = parameters

        self._close_session = False
        self.request_timeout = request_timeout

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
                    method,
                    ENDPOINT,
                    data=self._build_query(self._parameters),
                    headers=headers,
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

        return (await response.json())["array"]

    async def get_stations(self):
        data = await self._request()
        return [Station.from_dict(s) for s in data]

    async def get_station_by_id(self, id):
        stations = await self.get_stations()
        try:
            return next(filter(lambda d: d.id == id, stations))
        except Exception:
            raise StationsNotFoundException("Couldn't find specified station.")

    @staticmethod
    def _build_query(data) -> str:
        try:
            return f"region={REGIONS[data['region']]}\
                &province={data['province']}\
                &town={data['town']}\
                &carb="
        except KeyError as exception:
            raise RegionNotFoundException(
                "Error occurred while trying to find the region."
            ) from exception
