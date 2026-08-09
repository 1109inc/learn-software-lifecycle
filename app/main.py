import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.root_router import router as api_router
from app.core.settings import settings
from app.db.session import engine
from app.handlers.exception_handlers import register_exception_handlers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    logger.info("Application starting up")

    try:
        yield
    finally:
        logger.info("Application shutting down")
        await engine.dispose()


app = FastAPI(
    title="Learn Backend API",
    description="Production-grade FastAPI backend built for learning.",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_router)
