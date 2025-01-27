from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.activity.repository import ActivityRepository
from core.database.db_helper import db_helper
from core.database.models import Activity


async def get_activity_repository(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ActivityRepository:
    return ActivityRepository(session=session)


async def get_sub_activities(
    session: AsyncSession, activity: Activity, max_depth: int = 3, current_depth: int = 0
) -> list[Activity]:
    if current_depth >= max_depth:
        return []
    await session.refresh(activity, ["children"])
    children = activity.children
    sub_activities = children
    for child in children:
        sub_activities += await get_sub_activities(
            session=session, activity=child, current_depth=current_depth + 1
        )
    return sub_activities
