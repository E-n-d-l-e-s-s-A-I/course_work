from pydantic import BaseModel


class PathBase(BaseModel):
    distance: float
    max_height: float
    max_weight: float


class PathWithCities(PathBase):
    city_from_id: str
    city_to_id: str

class Path(PathWithCities):
    id: str

