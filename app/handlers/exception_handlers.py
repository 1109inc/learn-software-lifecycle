import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.error_codes import ErrorCode
from app.core.request_context import get_request_id
from app.exceptions.base import AppException
from app.schemas.errors import ErrorResponse, FieldError

logger = logging.getLogger(__name__)


def _error_response(
    status_code: int,
    code: ErrorCode,
    detail: str,
    fields: list[FieldError] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            code=code,
            detail=detail,
            request_id=get_request_id(),
            fields=fields,
        ).model_dump(mode="json"),
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return _error_response(exc.status_code, exc.error_code, exc.message)


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    fields = [
        FieldError(
            field=".".join(str(part) for part in error["loc"][1:]),
            message=error["msg"],
        )
        for error in exc.errors()
    ]

    logger.warning(
        "request validation failed",
        extra={
            "context": {
                "path": request.url.path,
                "errors": [f.model_dump() for f in fields],
            }
        },
    )

    return _error_response(
        HTTPStatus.UNPROCESSABLE_ENTITY,
        ErrorCode.VALIDATION_ERROR,
        "Request validation failed.",
        fields,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    return _error_response(
        exc.status_code,
        ErrorCode.HTTP_ERROR,
        str(exc.detail),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "unhandled exception",
        extra={"context": {"method": request.method, "path": request.url.path}},
    )

    return _error_response(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        ErrorCode.INTERNAL_SERVER_ERROR,
        "An internal error occurred.",
    )


def register_exception_handlers(app: FastAPI) -> None:
    # Starlette types handlers as accepting bare Exception; it only ever calls
    # each one with the type it was registered for, but the signature can't
    # express that.
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
