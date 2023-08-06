import asyncio

import aiohttp
import pytest

from pygtt import PyGTT, PyGTTConnectionError

from . import load_fixture


@pytest.mark.asyncio
async def test_request(aresponses):
    aresponses.add(response="OK")

    async with aiohttp.ClientSession() as session:
        pygtt = PyGTT(session=session, stop_name="512")
        r = await pygtt._request()
        assert r == "OK"


@pytest.mark.asyncio
async def test_404(aresponses):
    aresponses.add(response=aresponses.Response(status=404))

    async with aiohttp.ClientSession() as session:
        pygtt = PyGTT(session=session, stop_name="512")
        with pytest.raises(PyGTTConnectionError):
            await pygtt._request()


@pytest.mark.asyncio
async def test_builtin_session(aresponses):
    aresponses.add("OK")

    async with PyGTT(stop_name="512") as pygtt:
        with pytest.raises(PyGTTConnectionError):
            await pygtt._request()


@pytest.mark.asyncio
async def test_timeout(aresponses):
    async def response_handler(_):
        await asyncio.sleep(2)
        return aresponses.Response(body="Not important.")

    aresponses.add(response_handler)

    async with aiohttp.ClientSession() as session:
        pygtt = PyGTT(session=session, stop_name="512", request_timeout=1)
        with pytest.raises(PyGTTConnectionError):
            await pygtt._request()


@pytest.mark.asyncio
async def test_parse():
    pygtt = PyGTT(stop_name="512")
    pygtt._parse_data(load_fixture("sample.html"))
    assert pygtt._stop is not None
    assert len(pygtt._stop.bus_list)


@pytest.mark.asyncio
async def test_get_state(aresponses):
    aresponses.add(response=load_fixture("sample.html"))
    async with PyGTT(stop_name="512") as p:
        assert await p.get_state()
