from contextlib import asynccontextmanager
import asyncio
import logging
import threading

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.log_config import is_master_process, setup_logging, shutdown_logging
from app.common.log_consumer import consume_logs_forever
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
from app.services.common.thread_pool import thread_pool_service


ALLOWED_ORIGINS = ["*"] if settings.ENV in ["development", "preview"] else ["*"]
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logging()
    logger.info("Application starting up")
    if is_master_process():
        try:
            def run_log_consumer():
                asyncio.run(consume_logs_forever())

            threading.Thread(target=run_log_consumer, daemon=True).start()
            logger.info("[LogConsumer] Log consumer thread started (master process)")
        except Exception as exc:
            logger.warning(f"[LogConsumer] Failed to start log consumer thread: {exc}")
    yield
    if is_master_process():
        shutdown_logging()
    await close_db_engine()
    await redis_client.close()
    thread_pool_service.shutdown()
    logger.info("Application shutting down")


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
    async def api_exception_handler(request: Request, exc: APIException):
        logger.error(
            f"API Exception: {exc.status_code} - {exc.code} - {exc.detail}",
            extra={"request": f"{request.method} {request.url}"},
        )
        return ApiResponse.failed(
            message=exc.detail,
            body_code=exc.code,
            http_code=exc.status_code,
            data=exc.data,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(
            f"HTTP Exception: {exc.status_code} - {exc.detail}",
            extra={"request": f"{request.method} {request.url}"},
        )
        return ApiResponse.failed(
            message=exc.detail,
            body_code=exc.status_code,
            http_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(
            f"Validation Error: {exc.errors()}",
            extra={"request": f"{request.method} {request.url}"},
        )
        return ApiResponse.failed(
            message="Validation error",
            body_code=1001,
            http_code=status.HTTP_400_BAD_REQUEST,
            data=exc.errors(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(
            f"Unhandled Exception: {exc}",
            extra={"request": f"{request.method} {request.url}"},
        )
        return ApiResponse.failed(
            message="Internal server error",
            body_code=1005,
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
