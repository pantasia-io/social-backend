from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi import Depends

from app.user.schemas import AccessTokenResponse
from app.user.schemas import User
from app.user.utils import exchange_code_for_access_token
from app.user.utils import refresh_access_token
from app.user.utils import validate_user

router = APIRouter()


@router.get('/access_token', response_model=AccessTokenResponse)
async def exchange_token(code: str) -> Any:
    return await exchange_code_for_access_token(code=code)


@router.get('/refresh_token', response_model=AccessTokenResponse)
async def refresh_token(refresh_token: str) -> Any:
    return await refresh_access_token(refresh_token=refresh_token)


@router.get('/test')
async def test(user: User = Depends(validate_user)):
    return user
