from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.activity.repository import ActivityRepository
from api.api_v1.buildings.repository import BuildingRepository
from core.database.db_helper import db_helper
from core.database.models import Activity, Building

from ..activity.dependencies import get_activity_repository
from ..buildings.dependencies import get_building_repository
from .repository import OrganizationRepository
from .schemas import OrganizationSchema


async def get_organization_repository(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrganizationRepository:
    return OrganizationRepository(session=session)


async def get_organizations(
    repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    organization_data: Annotated[str, Path],
) -> OrganizationSchema | None:

    if organization_data.isdigit():
        organization = await repo.get_organizations_by_id(organization_id=int(organization_data))
    else:
        organization = await repo.get_organizations_by_name(organization_name=organization_data)
    if organization is not None:
        return organization
    raise HTTPException(status_code=404, detail="Organization not found")


async def get_building_by_id(
    repo: Annotated[BuildingRepository, Depends(get_building_repository)],
    building_id: Annotated[int, Path],
) -> Building:
    building = await repo.get_building(building_id=building_id)
    if building is not None:
        return building
    raise HTTPException(status_code=404, detail="Building not found")


async def get_activity_by_name(
    repo: Annotated[ActivityRepository, Depends(get_activity_repository)],
    activity_name: Annotated[str, Path],
) -> Activity:
    activity = await repo.get_activity(activity_name=activity_name)
    if activity is not None:
        return activity
    raise HTTPException(status_code=404, detail="Activity not found")
