from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator
from utils.validators import range_validator


class TruckBase(BaseModel):
    name: str
    speed: float
    weight: float
    max_cargo_weight: float
    height: float

    @field_validator("weight", "max_cargo_weight", mode="after")
    @classmethod
    def weight_validator(cls, value: float) -> float:
        return range_validator(value, "массы", 0, 10000)

    @field_validator("height", mode="after")
    @classmethod
    def height_validator(cls, value: float) -> float:
        return range_validator(value, "высоты", 0, 20)

    @field_validator("speed", mode="after")
    @classmethod
    def speed_validator(cls, value: float) -> float:
        return range_validator(value, "скорости", 0, 150)

    model_config = ConfigDict(from_attributes=True)


class TruckWithId(TruckBase):
    id: UUID
