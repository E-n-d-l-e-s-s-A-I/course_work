import heapq
import uuid

from api import crud_api
from fastapi import HTTPException
from schemas import Path, TaskInput, TaskOutput, Truck


def get_cargo_weight(task_input: TaskInput) -> float:
    task_weight = sum(
        crud_api.get_cargo(cargo.cargo_id).weight * cargo.cargo_count for cargo in task_input.cargos
    )
    return task_weight


def find_possible_trucks(cargo_weight: float) -> list[Truck]:
    trucks = crud_api.get_trucks()
    trucks = [truck for truck in trucks if truck.max_cargo_weight >= cargo_weight]
    return trucks


def filter_paths(paths: list[Path], weight: float, height: float) -> list[Path]:
    return [path for path in paths if path.max_height >= height and path.max_weight >= weight]


class PathNotFoundError(Exception):
    pass


def find_min_path(paths: list[Path], city_from: str, city_to: str) -> list[Path]:
    # Создаем граф (словарь смежности)
    graph: dict[str, list[tuple[float, str, Path]]] = {}
    for path in paths:
        graph.setdefault(path.city_from_id, []).append((path.distance, path.city_to_id, path))
        graph.setdefault(path.city_to_id, []).append(
            (path.distance, path.city_from_id, path)
        )  # Делаем двусторонним

    if city_from not in graph or city_to not in graph:
        raise PathNotFoundError("Один или оба города отсутствуют в доступных по грузоподемности маршрутах.")

    # Очередь приоритетов (мин-куча) с уникальным ID для сравнения
    priority_queue = [
        (0, str(uuid.uuid4()), city_from, [])
    ]  # (общая дистанция, уникальный ID, текущий город, список маршрутов)
    visited = set()

    while priority_queue:
        current_distance, _, current_city, current_path = heapq.heappop(priority_queue)

        if current_city in visited:
            continue
        visited.add(current_city)

        if current_city == city_to:
            return current_path  # Нашли кратчайший путь

        for distance, neighbor, path in graph.get(current_city, []):
            if neighbor not in visited:
                heapq.heappush(
                    priority_queue,
                    (
                        current_distance + distance,
                        str(uuid.uuid4()),
                        neighbor,
                        current_path + [path],
                    ),
                )

    raise PathNotFoundError("Маршрут между указанными городами не найден.")


def solve(task_input: TaskInput) -> TaskOutput:
    cargo_weight = get_cargo_weight(task_input)
    possible_trucks = find_possible_trucks(cargo_weight)
    paths = crud_api.get_paths()
    results: list[TaskOutput] = []

    if not possible_trucks:
        raise HTTPException(404, "Нет подходящих грузовиков по грузоподъемности.")
    for truck in possible_trucks:
        truck_with_cargo_weight = truck.weight + cargo_weight
        possible_paths = filter_paths(paths, truck_with_cargo_weight, truck.height)
        try:
            res_paths = find_min_path(
                possible_paths, task_input.city_from_id, task_input.city_to_id
            )
            results.append(
                TaskOutput(
                    paths=res_paths,
                    truck=truck,
                    time=round((sum(path.distance for path in res_paths) / truck.speed), 2),
                )
            )
        except PathNotFoundError as e:
            raise HTTPException(404, str(e)) from None

    if not results:
        raise HTTPException(404, "Нет доступных маршрутов")

    return min(results, key=lambda x: x.time)
