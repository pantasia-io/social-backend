from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from app.user.schemas import User
from app.user.utils import validate_user

router = APIRouter()


@router.get('/access_token')
async def get_access_token():
    return {'message': 'Return Access Token'}


@router.get('/refresh_token')
async def refresh_access_token():
    return {'message': 'Return Refreshed Access Token'}


@router.get('/test')
async def test(user: User = Depends(validate_user)):
    return user
