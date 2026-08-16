from pydantic import BaseModel, Field

from app.core.error_codes import ErrorCode


class FieldError(BaseModel):
    field: str = Field(description="Where the invalid value was in the request.")
    message: str = Field(description="Why it was rejected.")


class ErrorResponse(BaseModel):
    code: ErrorCode
    detail: str = Field(
        description="A message describing the error.",
        examples=["User with this email already exists."],
    )
    request_id: str | None = Field(
        default=None,
        description="Correlation ID for this request. Quote it when reporting a problem.",
    )
    fields: list[FieldError] | None = Field(
        default=None,
        description="Per-field validation errors, when applicable.",
    )
