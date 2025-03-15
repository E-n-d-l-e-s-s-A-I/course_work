from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class City(CityBase):
    id: str
