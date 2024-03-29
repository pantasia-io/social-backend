from __future__ import annotations

from fastapi import FastAPI

from app.common.router import router as common_router
from app.core.aio.client import async_client
from app.user.router import router as user_router
from app.wallet.router import router as wallet_router

app = FastAPI()

app.include_router(common_router, prefix='', tags=['Core'])

app.include_router(user_router, prefix='/user', tags=['User'])

app.include_router(wallet_router, prefix='/wallet', tags=['Wallet'])


@app.on_event('startup')
async def startup() -> None:
    # Initialize Aiohttp Connection
    async_client.start()
