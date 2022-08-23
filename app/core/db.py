from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URI, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


# DB Session Dependency
async def get_session() -> AsyncSession:
    async with async_session.begin() as session:
        yield session
