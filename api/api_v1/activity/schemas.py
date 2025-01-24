from pydantic import BaseModel, ConfigDict


class ActivityBaseSchema(BaseModel):
    name: str


class ActivitySchema(ActivityBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
