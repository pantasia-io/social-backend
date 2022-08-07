from __future__ import annotations

import aiohttp
import pytest

from app.core.aio.client import HttpClient


@pytest.mark.asyncio
async def test_client():
    client = HttpClient()
    assert client.session is None

    client.start()
    assert client.session is not None
    assert isinstance(client.session, aiohttp.ClientSession)

    assert client() == client.session

    await client.stop()

    assert client.session is None
