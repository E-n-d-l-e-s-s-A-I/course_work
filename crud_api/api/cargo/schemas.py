from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator
from utils.validators import range_validator


class CargoBase(BaseModel):
    name: str
    weight: float

    @field_validator("weight", mode="after")
    @classmethod
    def weight_validator(cls, value: float) -> float:
        return range_validator(value, "массы", 0, 10000)

    model_config = ConfigDict(from_attributes=True)


class CargoWithId(CargoBase):
    id: UUID
