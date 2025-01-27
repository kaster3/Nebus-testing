from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from api.api_v1.dependencies import static_auth_token
from core.database.models import Activity, Building, Organization

from .dependencies import (
    get_activity_by_name,
    get_building_by_id,
    get_organization_repository,
    get_organizations,
)
from .repository import OrganizationRepository
from .schemas import OrganizationSchema

router = APIRouter(
    prefix="/organizations",
    tags=["Organization"],
)


@router.get(
    "/by_building/{building_id}",
    response_model=list[OrganizationSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(static_auth_token)],
)
async def get_organizations_by_building(
    building: Annotated[Building, Depends(get_building_by_id)],
    repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
):
    return await repo.get_organizations_by_building(building=building)


@router.get(
    "/by_activity/{activity_name}",
    response_model=list[OrganizationSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(static_auth_token)],
)
async def get_organizations_by_activity(
    activity: Annotated[Activity, Depends(get_activity_by_name)],
    repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
):
    return await repo.get_organizations_by_activity(activity=activity)


@router.get(
    "/radius",
    response_model=list[OrganizationSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(static_auth_token)],
)
async def get_organizations_radius(
    repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    latitude: float = Query(..., description="Широта точки"),
    longitude: float = Query(..., description="Долгота точки"),
    radius: float = Query(..., description="Радиус в километрах"),
):
    organizations = await repo.get_organizations_by_radius(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
    )
    return organizations


@router.get(
    "/rectangle",
    response_model=list[OrganizationSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(static_auth_token)],
)
async def get_organizations_rectangle(
    repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    lower_left_latitude: float = Query(..., description="Широта нижнего левого угла"),
    lower_left_longitude: float = Query(..., description="Долгота нижнего левого угла"),
    upper_right_latitude: float = Query(..., description="Широта верхнего правого угла"),
    upper_right_longitude: float = Query(..., description="Долгота верхнего правого угла"),
):
    organizations = await repo.get_organizations_in_rectangle(
        lower_left_latitude=lower_left_latitude,
        lower_left_longitude=lower_left_longitude,
        upper_right_latitude=upper_right_latitude,
        upper_right_longitude=upper_right_longitude,
    )
    return organizations


@router.get(
    "/by_activity_with_sub",
    response_model=list[OrganizationSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(static_auth_token)],
)
async def get_organizations_with_subactivities(
    root_activity: Annotated[Activity, Depends(get_activity_by_name)],
    repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
):
    organizations = await repo.get_organizations_with_subactivities(
        root_activity=root_activity,
    )
    return organizations


@router.get(
    "/{organization_id_or_name}",
    response_model=OrganizationSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(static_auth_token)],
)
async def get_organization(
    organization: Annotated[Organization, Depends(get_organizations)],
):
    return organization
