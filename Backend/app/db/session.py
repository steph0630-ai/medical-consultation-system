from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session_local


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session_local = get_session_local()
    async with async_session_local() as session:
        yield session


@asynccontextmanager
async def transaction(db: AsyncSession):
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise


@asynccontextmanager
async def async_session():
    async_session_local = get_session_local()
    async with async_session_local() as session:
        try:
            yield session
        finally:
            await session.close()
