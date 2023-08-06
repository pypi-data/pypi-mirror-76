import aiohttp
import asyncio
from .consts import BASE_URL
from .models import Stop, Bus, BusTime
from .exceptions import PyGTTConnectionError
import async_timeout
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import copy


class PyGTT:
    def __init__(
        self,
        stop_name: str,
        session: aiohttp.ClientSession = None,
        request_timeout: int = 8,
    ) -> "PyGTT":
        self._stop = Stop(stop_name)
        self._session = session
        self._close_session = False
        self._request_timeout = request_timeout

    async def _request(self) -> None:
        """Handle the request to PyGTT."""

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self._request_timeout):
                response = await self._session.request(
                    "GET", BASE_URL.format(self._stop.name),
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise PyGTTConnectionError(
                "Timeout occurred while connecting to GTT."
            ) from exception
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as exception:
            raise PyGTTConnectionError(
                "Error occurred while connecting to GTT."
            ) from exception

        return await response.text()

    def _parse_data(self, data):
        """Parse the data from PyGTT."""
        self._stop.bus_list.clear()

        soup = BeautifulSoup(data, "html.parser")
        time_table = soup.findAll("table")[0]

        for row in time_table.findAll("tr"):

            for column in row.findAll("td"):
                if column.findAll("a"):
                    bus = Bus(column.find("a").text)
                    bus.time.clear()
                else:
                    time = datetime.strptime(
                        column.text.replace("*", "").strip(), "%H:%M"
                    )
                    time = time.replace(
                        year=datetime.now().year,
                        month=datetime.now().month,
                        day=datetime.now().day,
                    )

                    if time <= (datetime.now() + timedelta(minutes=1)):
                        time = time + timedelta(days=1)

                    bus.time.append(BusTime(time, "*" in column.text))
            self._stop.bus_list.append(copy.deepcopy(bus))
        return self._stop

    async def get_state(self):
        """Get the state of the stop."""
        self._stop = self._parse_data(await self._request())
        return self._stop

    async def close(self) -> None:
        """Close the session."""
        if self._close_session and self._session:
            await self._session.close()

    async def __aenter__(self) -> "PyGTT":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
