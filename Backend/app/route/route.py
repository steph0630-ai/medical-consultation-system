from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import close_db_engine
from app.exceptions.http_exceptions import APIException
from app.route.router_registry import (
    get_backoffice_routes,
    get_client_routes,
    get_common_routes,
    register_routes,
)
from app.schemas.response import ApiResponse
from app.services.common.redis import redis_client


ALLOWED_ORIGINS = ["*"] if settings.ENV in ["development", "preview"] else ["*"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await close_db_engine()
    await redis_client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routes(app, get_client_routes())
    register_routes(app, get_backoffice_routes())
    register_routes(app, get_common_routes())

    @app.exception_handler(APIException)
    async def api_exception_handler(_: Request, exc: APIException):
        return ApiResponse.failed(
            message=exc.detail,
            body_code=exc.code,
            http_code=exc.status_code,
            data=exc.data,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        return ApiResponse.failed(
            message=exc.detail,
            body_code=exc.status_code,
            http_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        return ApiResponse.failed(
            message="Validation error",
            body_code=1001,
            http_code=status.HTTP_400_BAD_REQUEST,
            data=exc.errors(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(_: Request, __: Exception):
        return ApiResponse.failed(
            message="Internal server error",
            body_code=1005,
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
