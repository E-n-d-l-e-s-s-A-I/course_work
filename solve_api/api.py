import requests as re
from schemas import Cargo, Path, Truck
from settings import settings


class CrudAPI:
    """Api для обращений к crud_api."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def get_trucks(self) -> list[Truck]:
        trucks_raw = re.get(self.api_endpoint + "/truck").json()
        trucks: list[Truck] = [Truck(**truck) for truck in trucks_raw]
        return trucks

    def get_cargo(self, cargo_id: str) -> Cargo:
        cargo_raw = re.get(self.api_endpoint + f"/cargo/{cargo_id}").json()
        return Cargo(**cargo_raw)

    def get_paths(self) -> list[Cargo]:
        paths_raw = re.get(self.api_endpoint + "/path").json()
        return [Path(**path_raw) for path_raw in paths_raw]


crud_api = CrudAPI(api_endpoint=settings.BACKEND_URL)
