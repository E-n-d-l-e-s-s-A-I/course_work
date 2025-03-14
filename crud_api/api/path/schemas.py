from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PathBase(BaseModel):
    city_from_id: UUID
    city_to_id: UUID
    distance: float
    max_height: float
    max_weight: float

    model_config = ConfigDict(from_attributes=True)


class PathWithId(PathBase):
    id: UUID
