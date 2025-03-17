from pydantic import BaseModel


class CargoWithCount(BaseModel):
    cargo_id: str
    cargo_count: int


class Task(BaseModel):
    city_from_id: str
    city_to_id: str
    cargos: list[CargoWithCount]


class Truck(BaseModel):
    id: str
    name: str
    speed: float
    weight: float
    max_cargo_weight: float
    height: float


class Path(BaseModel):
    id: str
    distance: float
    max_height: float
    max_weight: float
    city_from_id: str
    city_to_id: str


class TaskOutput(BaseModel):
    paths: list[Path]
    truck: Truck
    time: float
