from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.user.schemas import User
from app.user.utils import validate_user
from app.wallet.crud import connect_wallet_to_user
from app.wallet.schema import Wallet as WalletSchema
from app.wallet.utils import get_address_from_cbor
from app.wallet.utils import resolve_wallet_address
router = APIRouter()


@router.get('/connect_wallet', response_model=WalletSchema)
async def connect_wallet(
    cbor_address: str,
    user: User = Depends(validate_user),
    session: AsyncSession = Depends(get_session),
) -> Any:

    address = get_address_from_cbor(cbor_address)

    address_key = resolve_wallet_address(address)

    wallet = await connect_wallet_to_user(address=address_key, user=user, db=session)
    return wallet
