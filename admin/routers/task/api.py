import requests as re
from routers.task.schemas import Task


class SolveApi:
    """Api для обращений к эндпоинтам solve_api."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def solve(self, task: Task):
        solve_raw = re.post(self.api_endpoint + "/solve", json=task.model_dump()).json()
        # paths: list[Path] = [Path(**path) for path in path_raw]
        # return paths
