import pytest
from unittest.mock import AsyncMock
from app.services.user import UserService
from app.schemas.user import UserCreate
from app.models.user import User
from app.exceptions.user import UserAlreadyExistsError

@pytest.mark.asyncio
async def test_create_user_success():

    # Arrange

    repository = AsyncMock()

    user = UserCreate(
        name="Pragat",
        email="pragat@gmail.com",
    )

    created_user = User(
        id=1,
        name="Pragat",
        email="pragat@gmail.com"
    )

    repository.get_user_by_email.return_value = None
    repository.create_user.return_value = created_user

    service = UserService(
        user_repository=repository,
    )

    # Act

    result = await service.create_user(
        db=None,
        user=user,
    )

    # Assert

    assert result == created_user

    repository.get_user_by_email.assert_called_once_with(
        db=None,
        email=user.email,
    )

    repository.create_user.assert_called_once_with(
        db=None,
        user=user,
    )

@pytest.mark.asyncio
async def test_create_user_user_already_exists():

    # Arrange

    repository = AsyncMock()

    user = UserCreate(
        name="Pragat",
        email="pragat@gmail.com",
    )

    existing_user = User(
        id=1,
        name="Pragat",
        email="pragat@gmail.com",
    )

    repository.get_user_by_email.return_value = existing_user

    service = UserService(
        user_repository=repository,
    )

    # Act & Assert

    with pytest.raises(UserAlreadyExistsError):
        await service.create_user(
            db=None,
            user=user,
        )

    repository.get_user_by_email.assert_called_once_with(
        db=None,
        email=user.email,
    )

    repository.create_user.assert_not_called()