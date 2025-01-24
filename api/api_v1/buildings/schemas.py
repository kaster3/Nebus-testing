from pydantic import BaseModel, ConfigDict


class BuildingBaseSchema(BaseModel):
    city: str
    street: str
    house_number: str
    apartment_number: int | None
    latitude: float | None
    longitude: float | None


class BuildingSchema(BuildingBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
