from pydantic import BaseModel, ConfigDict

from api.api_v1.activity.schemas import ActivitySchema
from api.api_v1.buildings.schemas import BuildingSchema
from api.api_v1.phones.schemas import PhoneNumberSchema


class OrganizationBaseSchema(BaseModel):
    id: int
    name: str


class OrganizationSchema(OrganizationBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    building: BuildingSchema
    phone_numbers: list[PhoneNumberSchema]
    activities: list[ActivitySchema]
