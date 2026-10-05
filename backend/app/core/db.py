from collections.abc import AsyncIterator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.settings import get_settings


class Base(DeclarativeBase):
    pass


_settings = get_settings()
_url = _settings.database_url
_pool = {"poolclass": NullPool} if _settings.db_null_pool else {}
# One URL (postgresql+psycopg://) for both engines: async for the API, sync for Celery.
async_engine = create_async_engine(_url, pool_pre_ping=True, **_pool)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
sync_engine = create_engine(_url, pool_pre_ping=True, **_pool)
SyncSessionLocal = sessionmaker(sync_engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
