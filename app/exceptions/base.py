from app.core.error_codes import ErrorCode


class AppException(Exception):
    """
    Base class for all application exceptions.
    """

    error_code: ErrorCode

    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(message)
