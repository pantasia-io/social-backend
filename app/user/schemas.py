from __future__ import annotations

from pydantic import BaseModel


class DiscordUserData(BaseModel):
    id: str
    username: str


class DiscordData(BaseModel):
    user: DiscordUserData


class User(DiscordData):
    """
    Pantasia User
    """
    pass


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
