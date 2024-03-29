from __future__ import annotations

import aiohttp

from app.core.config import settings


class HttpClient:
    session: aiohttp.ClientSession = None

    def start(self):
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(force_close=True),
            timeout=aiohttp.ClientTimeout(
                total=settings.AIO_HTTP_CLIENT_TIMEOUT_SEC,
            ),
        )

    async def stop(self):
        await self.session.close()
        self.session = None

    def __call__(self) -> aiohttp.ClientSession:
        assert self.session is not None
        return self.session


async_client = HttpClient()
