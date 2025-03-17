import logging

from api import crud_api
from schemas import TaskInput, Truck


def get_cargo_weight(task_input: TaskInput) -> float:
    task_weight = sum(
        crud_api.get_cargo(cargo.cargo_id).weight * cargo.cargo_count for cargo in task_input.cargos
    )
    return task_weight


def find_possible_trucks(cargo_weight: float) -> list[Truck]:
    trucks = crud_api.get_trucks()
    trucks = [truck for truck in trucks if truck.max_cargo_weight >= cargo_weight]
    return trucks


def solve(task_input: TaskInput):
    cargo_weight = get_cargo_weight(task_input)
    possible_trucks = find_possible_trucks(cargo_weight)
    logging.warn(cargo_weight)
    logging.warn(possible_trucks)
