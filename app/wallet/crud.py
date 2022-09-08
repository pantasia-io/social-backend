from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models import Wallet


async def connect_wallet_to_user(
    address: str,
    user: User,
    db: AsyncSession,
) -> Wallet:
    wallet = await get_wallet_from_address(
        address=address,
        db=db,
    )

    if wallet is None:
        raise Exception('Wallet Not Found')

    wallet = await update_wallet_user(
        wallet=wallet,
        user=user,
        db=db,
    )
    return wallet


async def get_wallet_from_address(
    address: str,
    db: AsyncSession,
) -> Wallet | None:
    stmt = (
        select(Wallet)
        .where(Wallet.address == address)
    )
    wallet = (await db.scalars(stmt)).first()
    return wallet


async def update_wallet_user(
    wallet: Wallet,
    user: User,
    db: AsyncSession,
):
    wallet.user = user
    await db.flush()
    return wallet


async def get_user_connected_wallets(
    user: User,
    db: AsyncSession,
    limit: int = 20,
    offset: int = 0,
) -> list(Wallet):
    stmt = (
        select(Wallet)
        .where(Wallet.user == user)
        .limit(limit)
        .offset(offset)
    )
    wallets = (await db.scalars(stmt)).all()
    return wallets
