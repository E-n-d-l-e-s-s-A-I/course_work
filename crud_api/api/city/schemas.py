from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class CityWithId(CityBase):
    id: UUID
