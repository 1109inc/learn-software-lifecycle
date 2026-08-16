from http import HTTPStatus

from app.core.error_codes import ErrorCode


class AppException(Exception):
    """Base class for all application exceptions."""

    error_code: ErrorCode
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
