from fastapi import (
    APIRouter,
    Depends,
    status,
    Query,
    Path,
)
from app.db.session import get_db
from app.services.user import user_service
from app.schemas.user import (
    UserCreate, 
    UserResponse,
    UserUpdate
)
from app.schemas.errors import ErrorResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter(
    prefix = "/users",
    tags = ["users"],
)

@router.post(
    "",
    response_model=UserResponse,
    description="Create a new user.",
    summary="Create user",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "A user with the given email already exists.",
        },
    },
)
async def create_user(
    user : UserCreate,
    db:AsyncSession = Depends(get_db)
):
    return await user_service.create_user(
        db=db,
        user=user,
    )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="Get a user by ID.",
    summary="Get user by ID",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found.",
        },
    },
)
async def get_user_by_id(
    user_id: int = Path(
        ...,
        gt =0,
        description = "Unique identifier of the user.",
        example = 1,
    ),
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    return user

@router.get(
    "/",
    response_model=List[UserResponse],
    description="Get all users",
    summary="List of all users",

)
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    return await user_service.get_users(
        db=db,
    )

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    description="Update one or more fields of a user.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Email already exists.",
        },
    },
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.update_user(
        db=db,
        user_id=user_id,
        user_update=user_update,
    )

    return user