from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class UserRepository:
    async def create_user(
        self,
        db: AsyncSession,
        user: UserCreate,
    ) -> User:

        db_user = User(
            name=user.name,
            email=user.email,
        )

        db.add(db_user)

        await db.commit()

        await db.refresh(db_user)

        return db_user

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User | None:

        stmt = select(User).where(User.email == email)

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User | None:

        stmt = select(User).where(User.id == user_id)

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_users(
        self,
        db: AsyncSession,
    ) -> Sequence[User]:
        stmt = select(User).order_by(User.created_at.desc())

        result = await db.execute(stmt)

        return result.scalars().all()

    async def update_user(self, db: AsyncSession, user: User, user_update: UserUpdate) -> User:

        update_data = user_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        await db.commit()

        await db.refresh(user)

        return user

    async def delete_user(self, db: AsyncSession, user: User) -> None:

        await db.delete(user)

        await db.commit()
