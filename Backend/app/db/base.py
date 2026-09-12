from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.models import Base


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = None
AsyncSessionLocal = None


def get_engine():
    global engine
    if engine is None:
        engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            echo=True,
            future=True,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_timeout=30,
            max_overflow=10,
            pool_size=20,
        )
    return engine


def get_session_local():
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        AsyncSessionLocal = async_sessionmaker(
            bind=get_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return AsyncSessionLocal


def create_scheduler_engine():
    return create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
        future=True,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_timeout=30,
        max_overflow=5,
        pool_size=5,
    )


def create_scheduler_session_factory(scheduler_engine):
    return async_sessionmaker(
        bind=scheduler_engine, class_=AsyncSession, expire_on_commit=False
    )


async def close_db_engine():
    if engine is not None:
        await engine.dispose()
