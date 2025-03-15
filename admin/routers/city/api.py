import requests as re
from routers.city.schemas import City, CityBase


class CityApi:
    """Api для обращений к эндпоинтам городов."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint + "/city/"

    def get_cities(self) -> list[City]:
        cities_raw = re.get(self.api_endpoint).json()
        cities: list[City] = [City(**city) for city in cities_raw]
        return cities

    def get_city(self, id: str) -> City:
        city_raw = re.get(self.api_endpoint + id).json()
        return City(**city_raw)

    def create_city(self, city_data: CityBase) -> bool:
        response = re.post(self.api_endpoint, json=city_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def update_city(self, id: str, city_data: CityBase) -> bool:
        response = re.put(self.api_endpoint + str(id), json=city_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def delete_city(self, id: str) -> bool:
        response = re.delete(self.api_endpoint + str(id))
        if response.status_code != 200:
            raise Exception(response.text)

        return True
