from __future__ import annotations

import datetime

from pydantic import BaseModel


class DiscordUserData(BaseModel):
    id: str
    username: str


class DiscordData(BaseModel):
    user: DiscordUserData


class User(BaseModel):
    """
    Pantasia User
    """
    id: int
    alias: str
    datetime_created: datetime.datetime

    class Config:
        orm_mode = True


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
