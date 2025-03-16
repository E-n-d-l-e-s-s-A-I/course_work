from routers.cargo.api import CargoApi
from routers.city.api import CityApi
from routers.path.api import PathApi
from routers.task.api import SolveApi
from routers.truck.api import TruckApi
from settings import settings


class CrudAPI:
    """Api для обращений к crud_api."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
        self.city = CityApi(api_endpoint)
        self.truck = TruckApi(api_endpoint)
        self.cargo = CargoApi(api_endpoint)
        self.path = PathApi(api_endpoint)


class SolveAPI:
    """Api для обращений к solve_api."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
        self.task = SolveApi(api_endpoint)


crud_api = CrudAPI(api_endpoint=settings.BACKEND_URL)
solve_api = SolveAPI(api_endpoint=settings.SOLVE_API_URL)
