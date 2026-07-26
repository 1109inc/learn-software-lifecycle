from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)

from app.exceptions.user import (
    UserAlreadyExistsError,
    UserNotFoundError
)
class UserService:

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    async def create_user(
        self,
        db: AsyncSession,
        user: UserCreate,
    ) -> User:
        
        existing_user = await self.user_repository.get_user_by_email(
            db=db,
            email=user.email
        )

        if existing_user:
            raise UserAlreadyExistsError(email=user.email)
        
        return await self.user_repository.create_user(
            db=db,
            user=user,
        )

    async def get_user_by_id(
        self,
        db: AsyncSession,
        user_id: int
    ) -> User:
        
        existing_user = await self.user_repository.get_user_by_id(
            db=db,
            user_id=user_id
        )

        if not existing_user:
            raise UserNotFoundError(user_id=user_id)
        
        return existing_user

    async def get_users(
        self,
        db:AsyncSession,
    ) -> list[User]:
        users = await self.user_repository.get_users(
            db=db,
        )

        return users

    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        user_update:UserUpdate
    ) -> User:

        existing_user = await self.user_repository.get_user_by_id(
            db=db,
            user_id=user_id,
        )

        if not existing_user:
            raise UserNotFoundError(user_id=user_id)

        if user_update.email is not None:

            existing_email = await self.user_repository.get_user_by_email(
                db=db,
                email=user_update.email,
            )

            if existing_email and existing_email.id != existing_user.id:
                raise UserAlreadyExistsError(email=user_update.email)
            

        return await self.user_repository.update_user(
            db=db,
            user=existing_user,
            user_update=user_update
        )

    async def delete_user(
        self,
        db: AsyncSession,
        user_id: int
    ) -> None:

        existing_user = await self.user_repository.get_user_by_id(
            db=db,
            user_id=user_id,
        )

        if not existing_user:
            raise UserNotFoundError(user_id=user_id)

        await self.user_repository.delete_user(
            db=db,
            user=existing_user
        )


user_service = UserService(
    user_repository=UserRepository(),
)