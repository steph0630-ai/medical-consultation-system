from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.db import Base, engine
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    # ponytail: create_all is enough for the first schema; use Alembic before schema changes.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="智能医疗咨询系统", lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1", tags=["client-auth"])


@app.get("/api/v1/config/health")
async def health() -> dict:
    return {
        "code": 200,
        "message": "success",
        "data": {"status": "healthy", "services": {"api": "up"}},
    }
