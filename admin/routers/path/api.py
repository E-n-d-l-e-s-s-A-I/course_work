import requests as re
from routers.path.schemas import Path, PathBase, PathWithCities


class PathApi:
    """Api для обращений к эндпоинтам путей."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint + "/path/"

    def get_paths(self) -> list[Path]:
        path_raw = re.get(self.api_endpoint).json()
        paths: list[Path] = [Path(**path) for path in path_raw]
        return paths

    def get_path(self, id: str) -> Path:
        path_raw = re.get(self.api_endpoint + id).json()
        return Path(**path_raw)

    def create_path(self, path_data: PathWithCities) -> bool:
        response = re.post(self.api_endpoint, json=path_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def update_path(self, id: str, path_data: PathBase) -> bool:
        response = re.put(self.api_endpoint + str(id), json=path_data.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)

        return True

    def delete_path(self, id: str) -> bool:
        response = re.delete(self.api_endpoint + str(id))
        if response.status_code != 200:
            raise Exception(response.text)

        return True
