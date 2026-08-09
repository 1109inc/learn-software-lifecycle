from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.schemas.errors import ErrorResponse
from app.services.health import health_service

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
    description="Returns 200 while the process is running. Checks no dependencies.",
)
async def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
    description="Returns 200 if the app can serve traffic, 503 if the database is unreachable.",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Database is unavailable.",
        },
    },
)
async def readiness(db: DbSession) -> dict[str, str]:
    await health_service.check_database(db=db)
    return {"status": "ready", "database": "ok"}
