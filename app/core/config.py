from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseSettings
from pydantic import PostgresDsn
from pydantic import validator


class Settings(BaseSettings):
    ###################
    # General
    ###################
    # loggings
    LOG_LEVEL: str = 'INFO'

    ###################
    # AIO Http Client
    ###################
    AIO_HTTP_CLIENT_TIMEOUT_SEC: int = 5

    ###################
    # Discord
    ###################
    DISCORD_API_ENDPOINT: str = 'https://discord.com/api/v10'
    DISCORD_REDIRECT_URL: str = 'https://www.google.com/'
    DISCORD_CLIENT_ID: str = '1005891636905123973'
    DISCORD_CLIENT_SECRET: str

    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = 'postgres'
    DATABASE_URI: PostgresDsn | None = None

    @validator('DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()

###
# Logging
###
logger = logging.getLogger('gunicorn.error')
logger.setLevel(settings.LOG_LEVEL)
