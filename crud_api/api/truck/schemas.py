from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TruckBase(BaseModel):
    name: str
    speed: float
    weight: float
    max_cargo_weight: float
    height: float

    model_config = ConfigDict(from_attributes=True)


class TruckWithId(TruckBase):
    id: UUID
