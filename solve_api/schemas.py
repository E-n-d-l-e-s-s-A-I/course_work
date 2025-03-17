from typing import Self

from pydantic import BaseModel, model_validator


class CargoWithCount(BaseModel):
    cargo_id: str
    cargo_count: int


class TaskInput(BaseModel):
    city_from_id: str
    city_to_id: str
    cargos: list[CargoWithCount]

    @model_validator(mode="after")
    def check_path(self) -> Self:
        if self.city_from_id == self.city_to_id:
            raise ValueError("Город отправления не может совпадать с городом прибытия")
        return self


class City(BaseModel):
    id: str
    name: str


class Truck(BaseModel):
    id: str
    name: str
    speed: float
    weight: float
    max_cargo_weight: float
    height: float


class Cargo(BaseModel):
    id: str
    name: str
    weight: float


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
