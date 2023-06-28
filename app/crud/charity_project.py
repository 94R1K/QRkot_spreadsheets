from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharity(CRUDBase):

    @staticmethod
    async def get_charity_id_by_name(
            charity_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_name
            )
        )
        return db_charity_id.scalars().first()

    @staticmethod
    async def get_projects_by_completion_rate(
            session: AsyncSession
    ) -> List[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )
        return sorted(
            projects.scalars().all(),
            key=lambda obj: obj.close_date - obj.create_date
        )


charity_crud = CRUDCharity(CharityProject)
