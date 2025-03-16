from pydantic import BaseModel


class CargoWithCount(BaseModel):
    cargo_id: str
    cargo_count: int


class Task(BaseModel):
    city_from_id: str
    city_to_id: str
    cargos: list[CargoWithCount]
