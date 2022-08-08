from __future__ import annotations

from fastapi import HTTPException
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.aio.client import async_client
from app.user.crud import get_or_create_user_discord
from app.user.schemas import DiscordData
from app.user.schemas import User

bearer = HTTPBearer(auto_error=False)


async def validate_user(
    bearer: HTTPAuthorizationCredentials = Security(bearer),
) -> User:
    """
    Will perform authentication:
    1. Check for Bearer Token, if present, validate with discord.
    2. Else, raise exception

    Once validated, retrieve discord user data and using it to retrieve pantasia
    user. Returns a User object
    """
    if bearer is not None:
        discord_user_data = get_auth_info(bearer)
        return get_or_create_user_discord(discord_user_data)

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED, detail='No Credentials is provided',
    )


async def get_auth_info(bearer: str) -> DiscordData | ValidationError:
    response = await async_client.session.get(
        'https://discord.com/api/v10/oauth2/@me',
        headers={'Authorization': f'Bearer {bearer}'},
    )
    data = await response.json()
    return DiscordData(**data)
