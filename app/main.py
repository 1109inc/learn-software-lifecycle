from fastapi import FastAPI

from app.api.root_router import router as api_router
from app.core.settings import settings
from app.handlers.exception_handlers import register_exception_handlers

app = FastAPI(
    title="Learn Backend API",
    description="Production-grade FastAPI backend built for learning.",
    version="1.0.0",
    debug=settings.DEBUG,
)

register_exception_handlers(app)

app.include_router(api_router)
