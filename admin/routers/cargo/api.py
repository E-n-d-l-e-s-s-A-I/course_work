import requests as re
from routers.cargo.schemas import Cargo, CargoBase


class CargoApi:
    """Api для обращений к эндпоинтам грузов."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint + "/cargo/"

    def get_cargos(self) -> list[Cargo]:
        cargo_raw = re.get(self.api_endpoint).json()
        cargos: list[Cargo] = [Cargo(**cargo) for cargo in cargo_raw]
        return cargos

    def get_cargo(self, id: str) -> Cargo:
        cargo_raw = re.get(self.api_endpoint + id).json()
        return Cargo(**cargo_raw)

    def create_cargo(self, cargo_data: CargoBase) -> bool:
        response = re.post(self.api_endpoint, json=cargo_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def update_cargo(self, id: str, cargo_data: CargoBase) -> bool:
        response = re.put(self.api_endpoint + str(id), json=cargo_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def delete_cargo(self, id: str) -> bool:
        response = re.delete(self.api_endpoint + str(id))
        if response.status_code != 200:
            raise Exception(response.text)

        return True
