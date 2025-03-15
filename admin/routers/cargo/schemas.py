from pydantic import BaseModel


class CargoBase(BaseModel):
    name: str
    weight: float


class Cargo(CargoBase):
    id: str
