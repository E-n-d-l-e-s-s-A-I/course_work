from routers.core_api import crud_api


def get_cargos_names() -> list[str]:
    """
    Возвращает названия всех грузов.

    Returns:
        list[str]: названия грузов.
    """
    return [cargo.name for cargo in crud_api.cargo.get_cargos()]


def get_cargo_id_by_name(cargo_name: str):
    """
    Возвращает id груза по названию.
    Args:
        city_name (str): Название груза.

    Returns:
        str: id груза.
    """
    return list(filter(lambda x: x.name == cargo_name, crud_api.cargo.get_cargos()))[0].id
