from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict, 
    EmailStr, 
    Field
)


class UserBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="The name of the user.",
    )
    email: EmailStr = Field(
        description="Unique email address of the user.",
        examples=["user@example.com"]
    )


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="The name of the user.",
    )

    email: EmailStr | None = Field(
        default=None,
        description="Unique email address of the user.",
        examples=["user@example.com"],
    )