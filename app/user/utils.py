from __future__ import annotations

from fastapi import HTTPException
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.aio.client import async_client
from app.core.config import settings
from app.user.crud import get_or_create_user_discord
from app.user.schemas import AccessTokenResponse
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
        discord_user_data = await get_auth_info(
            access_token=bearer.credentials,
        )
        return get_or_create_user_discord(discord_user_data)

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED, detail='No Credentials is provided',
    )


async def get_auth_info(access_token: str) -> DiscordData | ValidationError:
    response = await async_client.session.get(
        f'{settings.discord_api_endpoint}/oauth2/@me',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    data = await response.json()
    return DiscordData(**data)


async def exchange_code_for_access_token(code: str) -> AccessTokenResponse:
    payload = {
        'client_id': settings.discord_client_id,
        'client_secret': settings.discord_client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.discord_redirect_url,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = await async_client.session.post(
        f'{settings.discord_api_endpoint}/oauth2/token',
        headers=headers,
        data=payload,
    )

    response.raise_for_status()

    data = await response.json()
    return AccessTokenResponse(**data)


async def refresh_access_token(refresh_token: str) -> AccessTokenResponse:
    payload = {
        'client_id': settings.discord_client_id,
        'client_secret': settings.discord_client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = await async_client.session.post(
        f'{settings.discord_api_endpoint}/oauth2/token',
        headers=headers,
        data=payload,
    )

    response.raise_for_status()

    data = await response.json()
    return AccessTokenResponse(**data)
