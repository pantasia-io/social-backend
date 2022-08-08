from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get('/access_token')
async def get_access_token():
    return {'message': 'Return Access Token'}


@router.get('/refresh_token')
async def refresh_access_token():
    return {'message': 'Return Refreshed Access Token'}
