from __future__ import annotations

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
    pass
