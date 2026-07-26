from app.core.error_codes import ErrorCode
from app.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    error_code = ErrorCode.USER_ALREADY_EXISTS

    def __init__(
        self,
        email: str,
    ) -> None:
        super().__init__(
            f"User with email '{email}' already exists."
        )

class UserNotFoundError(AppException):
    error_code = ErrorCode.USER_NOT_FOUND

    def __init__(
        self,
        user_id: int,
    ) -> None:
        super().__init__(
            f"User with ID '{user_id}' not found."
        )