from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from api.api_v1.activity.dependencies import get_sub_activities
from core.database.models import Activity, Building, Organization
from core.settings import EARTH_RADIUS_KM


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _base_query(self):
        return select(Organization).options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
            joinedload(Organization.building),
        )

    async def get_organization_by_id(self, organization_id: int) -> Organization | None:
        stmt = self._base_query().where(Organization.id == organization_id)
        organization = await self.session.scalar(stmt)
        return organization

    async def get_organization_by_name(self, organization_name: str) -> Organization | None:
        stmt = self._base_query().where(Organization.name == organization_name)
        organization = await self.session.scalar(stmt)
        return organization

    async def get_organizations_by_building(self, building: Building) -> list[Organization]:
        stmt = self._base_query().where(Organization.building_id == building.id)
        organizations = await self.session.scalars(stmt)
        return list(organizations)

    async def get_organizations_by_activity(self, activity: Activity) -> list[Organization]:
        stmt = (
            select(Organization).join(Organization.activities).where(Activity.id == activity.id)
        ).options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.building),
        )
        organizations = await self.session.scalars(stmt)
        return list(organizations)

    async def get_organizations_in_rectangle(
        self,
        lower_left_latitude: float,
        lower_left_longitude: float,
        upper_right_latitude: float,
        upper_right_longitude: float,
    ) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Building)
            .filter(
                Building.latitude >= lower_left_latitude,
                Building.latitude <= upper_right_latitude,
                Building.longitude >= lower_left_longitude,
                Building.longitude <= upper_right_longitude,
            )
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
            )
        )
        organizations = await self.session.scalars(stmt)
        return list(organizations)

    async def get_organizations_by_radius(
        self, latitude: float, longitude: float, radius: float
    ) -> list[Organization]:

        stmt = (
            select(Organization)
            .join(Building)
            .filter(
                (
                    EARTH_RADIUS_KM
                    * func.acos(
                        func.least(
                            1.0,
                            func.greatest(
                                func.sin(func.radians(latitude))
                                * func.sin(func.radians(Building.latitude))
                                + func.cos(func.radians(latitude))
                                * func.cos(func.radians(Building.latitude))
                                * func.cos(
                                    func.radians(Building.longitude) - func.radians(longitude)
                                ),
                                -1.0,
                            ),
                        )
                    )
                )
                <= radius
            )
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
            )
        )
        organizations = await self.session.scalars(stmt)
        return list(organizations)

    async def get_organizations_with_subactivities(
        self,
        root_activity: Activity,
    ) -> list[Organization]:

        all_activities = [root_activity] + await get_sub_activities(
            self.session,
            root_activity,
        )

        activity_ids = {activity.id for activity in all_activities}

        stmt = (
            select(Organization)
            .join(Organization.activities)
            .filter(Activity.id.in_(activity_ids))
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
            )
        )
        organizations = await self.session.scalars(stmt)
        return list(organizations)
