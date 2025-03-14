from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CargoBase(BaseModel):
    name: str
    weight: float

    model_config = ConfigDict(from_attributes=True)


class CargoWithId(CargoBase):
    id: UUID
