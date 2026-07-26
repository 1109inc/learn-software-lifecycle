from app.core.error_codes import ErrorCode
from app.exceptions.base import AppException


class DatabaseUnavailableError(AppException):
    error_code = ErrorCode.DATABASE_UNAVAILABLE

    def __init__(self) -> None:
        super().__init__(
            "Database is currently unavailable."
        )