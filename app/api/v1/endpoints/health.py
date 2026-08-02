from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.services.health import health_service

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the health status of the application.",
)
async def health(db: DbSession):
    await health_service.check_database(db=db)
    return {"status": "healthy", "database": "healthy"}
