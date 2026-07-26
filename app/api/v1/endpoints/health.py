from fastapi import (
    APIRouter,
    status, 
    Depends
)
from app.db.session import get_db
from app.services.health import health_service

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the health status of the application.",
)
async def health(
    db: AsyncSession = Depends(get_db)
):
    await health_service.check_database(
        db=db
    )

    return {
        "status": "healthy",
        "database": "healthy",
    }