from routers.task.schemas import Task


class SolveApi:
    """Api для обращений к эндпоинтам solve_api."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint + "/path/"

    def solve(self, task: Task):
        pass
        # path_raw = re.get(self.api_endpoint).json()
        # paths: list[Path] = [Path(**path) for path in path_raw]
        # return paths
