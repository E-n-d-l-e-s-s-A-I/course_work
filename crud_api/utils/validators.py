from math import inf


def range_validator(value: float, entity: str, start: float = -inf, end: float = inf) -> float:
    """
    Валидатор, проверяющий что число принадлежит диапазоны [start, end].

    Args:
        value (float): Значение.
        start (float): Начало интервала.
        end (float): Конец интервала.

    Raises:
        ValueError: Значение не принадлежит диапазону.

    Returns:
        float: Провалидированное значение.
    """

    if value < start or value > end:
        raise ValueError(f"Значение {entity} должно принадлежать диапазону [{start}, {end}]")
    return value
