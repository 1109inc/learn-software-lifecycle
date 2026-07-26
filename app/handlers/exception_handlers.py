from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.responses import JSONResponse

from app.exceptions.base import AppException
from app.exceptions.database import DatabaseUnavailableError
from app.exceptions.user import UserAlreadyExistsError,UserNotFoundError
from app.schemas.errors import ErrorResponse


EXCEPTION_STATUS_CODE_MAP = {
    UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    DatabaseUnavailableError: status.HTTP_503_SERVICE_UNAVAILABLE,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
}


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    status_code = EXCEPTION_STATUS_CODE_MAP.get(
        type(exc),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            code=exc.error_code,
            detail=str(exc),
        ).model_dump(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )