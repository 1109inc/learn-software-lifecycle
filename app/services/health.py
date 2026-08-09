from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.database import DatabaseUnavailableError


class HealthService:
    async def check_database(
        self,
        db: AsyncSession,
    ) -> None:
        """
        Check whether the database is reachable.

        Raises:
            DatabaseUnavailableError: if the database cannot be reached.
        """

        try:
            await db.execute(text("SELECT 1"))
        except SQLAlchemyError as exc:
            raise DatabaseUnavailableError() from exc


health_service = HealthService()
