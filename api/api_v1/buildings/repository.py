from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Building


class BuildingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_building(self, building_id: int) -> Building | None:
        building = await self.session.get(Building, building_id)
        return building
