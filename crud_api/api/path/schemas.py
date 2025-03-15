from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from utils.validators import range_validator


class PathBase(BaseModel):
    city_from_id: UUID
    city_to_id: UUID
    distance: float
    max_height: float
    max_weight: float

    @field_validator("max_weight", mode="after")
    @classmethod
    def weight_validator(cls, value: float) -> float:
        return range_validator(value, 0, 20000)

    @field_validator("max_height", mode="after")
    @classmethod
    def height_validator(cls, value: float) -> float:
        return range_validator(value, 0, 20)

    @field_validator("distance", mode="after")
    @classmethod
    def distance_validator(cls, value: float) -> float:
        return range_validator(value, 0)

    @model_validator(mode="after")
    def check_path(self) -> Self:
        if self.city_from_id == self.city_to_id:
            raise ValueError("Город отправления не может совпадать с городом прибытия")
        return self

    model_config = ConfigDict(from_attributes=True)


class PathWithId(PathBase):
    id: UUID
