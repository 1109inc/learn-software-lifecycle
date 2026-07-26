from app.api.v1.v1_router import router as v1_router
from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
)

router.include_router(v1_router)