from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import ConnectionType
from app.models import SocialConnection
from app.models import User
from app.user.schemas import DiscordData
from app.user.schemas import User as UserSchema


async def get_or_create_user_discord(db: AsyncSession, data: DiscordData) -> UserSchema:
    # Read by connection id
    connection = await get_discord_connection_by_id(
        db=db, connection_id=data.user.id,
    )

    if connection is not None:
        # Get user from connection object and return
        return connection.user
    else:
        # Create User
        user = await create_user(db=db, alias=data.user.username)

        # Create Social Connection
        _ = await create_discord_connection(db, data=data, user=user)

        return user


async def create_user(
    db: AsyncSession,
    alias: str | None = None,
) -> User:
    new_user = User(alias=alias)
    db.add(new_user)
    await db.flush()
    return new_user


async def get_discord_connection_by_id(
    db: AsyncSession,
    connection_id: str,
) -> SocialConnection | None:
    stmt = (
        select(SocialConnection)
        .where(SocialConnection.connection_id == connection_id)
        .options(selectinload(SocialConnection.user))  # Eager Load User
    )
    connection = (await db.scalars(stmt)).first()
    return connection


async def create_discord_connection(
    db: AsyncSession,
    data: DiscordData,
    user: User,
):

    discord_connection = SocialConnection(
        user=user,
        connection_id=data.user.id,
        connection_type=ConnectionType.DISCORD,
    )
    db.add(discord_connection)
    await db.flush()

    return discord_connection
