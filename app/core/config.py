from __future__ import annotations

import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    ###################
    # General Settings
    ###################
    # loggings
    log_level: str = 'INFO'

    ###################
    # AIO Http Client Settings
    ###################
    aiohttp_client_session_timeout_sec: int = 5


settings = Settings()

###
# Logging
###
logger = logging.getLogger('gunicorn.error')
logger.setLevel(settings.log_level)
