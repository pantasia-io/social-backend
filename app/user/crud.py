from __future__ import annotations

from app.user.schemas import DiscordData
from app.user.schemas import User


def get_or_create_user_discord(data: DiscordData) -> User:
    return User()
