import requests as re
from routers.truck.schemas import Truck, TruckBase


class TruckApi:
    """Api для обращений к эндпоинтам грузовиков."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint + "/truck/"

    def get_trucks(self) -> list[Truck]:
        cities_raw = re.get(self.api_endpoint).json()
        cities: list[Truck] = [Truck(**city) for city in cities_raw]
        return cities

    def get_truck(self, id: str) -> Truck:
        city_raw = re.get(self.api_endpoint + id).json()
        return Truck(**city_raw)

    def create_truck(self, truck_data: TruckBase) -> bool:
        response = re.post(self.api_endpoint, json=truck_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def update_truck(self, id: str, truck_data: TruckBase) -> bool:
        response = re.put(self.api_endpoint + str(id), json=truck_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def delete_truck(self, id: str) -> bool:
        response = re.delete(self.api_endpoint + str(id))
        if response.status_code != 200:
            raise Exception(response.text)

        return True
