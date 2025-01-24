from pydantic import BaseModel, ConfigDict


class PhoneNumberBaseSchema(BaseModel):
    number: str
    organization_id: int


class PhoneNumberSchema(PhoneNumberBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
