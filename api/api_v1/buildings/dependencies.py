from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.buildings.repository import BuildingRepository
from core.database.db_helper import db_helper


async def get_building_repository(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BuildingRepository:
    return BuildingRepository(session=session)
