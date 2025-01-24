from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Activity


class ActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_activity(self, activity_name: str) -> Activity | None:
        stmt = select(Activity).where(Activity.name == activity_name)
        activity = await self.session.scalar(stmt)
        return activity
