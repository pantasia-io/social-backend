from __future__ import annotations

import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    ###################
    # General
    ###################
    # loggings
    log_level: str = 'INFO'

    ###################
    # AIO Http Client
    ###################
    aiohttp_client_session_timeout_sec: int = 5

    ###################
    # Discord
    ###################
    discord_api_endpoint: str = 'https://discord.com/api/v10'
    discord_redirect_url: str = 'https://www.google.com/'
    discord_client_id: str = '1005891636905123973'
    discord_client_secret: str


settings = Settings()

###
# Logging
###
logger = logging.getLogger('gunicorn.error')
logger.setLevel(settings.log_level)
