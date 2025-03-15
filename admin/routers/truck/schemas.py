from pydantic import BaseModel


class TruckBase(BaseModel):
    name: str
    speed: float
    weight: float
    max_cargo_weight: float
    height: float


class Truck(TruckBase):
    id: str
