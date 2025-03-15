from routers.cargo.api import CargoApi
from routers.city.api import CityApi
from routers.truck.api import TruckApi
from settings import settings


class API:
    """Api для обращений к crud_api."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
        self.city = CityApi(api_endpoint)
        self.truck = TruckApi(api_endpoint)
        self.cargo = CargoApi(api_endpoint)


api = API(api_endpoint=settings.BACKEND_URL)
