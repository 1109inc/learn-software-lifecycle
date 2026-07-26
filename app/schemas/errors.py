from pydantic import (
    BaseModel,
    Field
)

from app.core.error_codes import ErrorCode

class ErrorResponse(BaseModel):
    code: ErrorCode
    detail: str = Field(
        description="A message describing the error.",
        example="User with this email already exists."
    )