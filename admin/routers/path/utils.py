from routers.core_api import api
from routers.path.schemas import Path


def get_city_name(city_id: str) -> str:
    """
    Возвращает название города.

    Args:
        city_id (str): id города.

    Returns:
        str: Название города.
    """
    return api.city.get_city(id=city_id).name

def get_path_name(path: Path) -> str:
    """
    Возвращает название пути

    Args:
        id (Path): Путь.

    Returns:
        str: Название пути.
    """
    city_to_name = get_city_name(city_id=path.city_to_id)
    city_from_name = get_city_name(city_id=path.city_from_id)

    path_name = " - ".join(sorted([city_to_name, city_from_name]))
    return path_name


def get_cities_names() -> list[str]:
    """
    Возвращает названия всех городов.

    Returns:
        list[str]: Названия всех городов.
    """
    return [city.name for city in api.city.get_cities()]

def get_city_id_by_name(city_name: str) -> str:
    """
    Возвращает id города по названию.
    Args:
        city_name (str): Название города.

    Returns:
        str: id города.
    """
    return list(filter(lambda x: x.name == city_name, api.city.get_cities()))[0].id
