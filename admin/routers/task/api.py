import requests as re
from routers.task.schemas import Task, TaskOutput


class SolveApi:
    """Api для обращений к эндпоинтам solve_api."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def solve(self, task: Task) -> TaskOutput:
        response = re.post(self.api_endpoint + "/solve", json=task.model_dump())
        if response.status_code != 200:
            raise Exception(response.text)
        return TaskOutput(**response.json())
