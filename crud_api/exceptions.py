import re
from typing import Any

from fastapi import HTTPException
from models import Base


def extract_entity_name(error_message: str, pattern: str) -> str:
    """
    Функция для извлечения человекочитаемого имя сущности из сообщения об ошибки,
        генерируемого sqlalchemy.

    Args:
        error_message (str): сообщение об ошибки.
        pattern (str): регулярное выражение для поиска, имя таблицы должно быть в первой группе.

    Returns:
        str: Извлеченное имя таблицы или пустая строка.
    """
    search_res = re.search(pattern, error_message)
    if not search_res:
        return ""
    table_name = search_res.group(1)
    readable_name: str = Base.metadata.tables[table_name].info["readable_name"]
    return readable_name


class DBIntegrityException(HTTPException):
    """Класс для исключения нарушения целостности бд."""

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(409, detail, headers)
        if "violates foreign key constraint" not in detail:
            return
        if "delete on table" in detail:
            raise ForeignKeyConstraintViolationException(detail, headers)
        if "insert or update on table" in detail:
            raise InvalidForeignKeyException(detail, headers)


class ForeignKeyConstraintViolationException(HTTPException):
    """
    Класс для исключения, возникающее при попытке
    удалить объект с существующими связанными объектами.
    """

    EXCEPTION_MESSAGE_TEMPLATE = (
        "Невозможно удалить сущность '{entity_name}',"
        " т.к. она связана с сущностью '{relative_entity_name}'."
    )

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        entity_name = extract_entity_name(detail, r'update or delete on table "([a-zA-Z_]*)"')
        relative_entity_name = extract_entity_name(
            detail,
            r'is still referenced from table "([a-zA-Z_]*)"',
        )
        if entity_name and relative_entity_name:
            detail = ForeignKeyConstraintViolationException.EXCEPTION_MESSAGE_TEMPLATE.format(
                entity_name=entity_name,
                relative_entity_name=relative_entity_name,
            )
        super().__init__(409, detail, headers)


class InvalidForeignKeyException(HTTPException):
    """Класс для исключения, возникающее при попытке установить несуществующий внешний ключ."""

    EXCEPTION_MESSAGE_TEMPLATE = "Сущность '{entity_name}' по вторичному ключу не существует."

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        entity_name = extract_entity_name(detail, r'is not present in table "([a-zA-Z_]*)"')
        if entity_name:
            detail = InvalidForeignKeyException.EXCEPTION_MESSAGE_TEMPLATE.format(
                entity_name=entity_name,
            )
        super().__init__(409, detail, headers)


class EntityNotFoundException(HTTPException):
    """Класс для исключения отсутствия сущности."""

    EXCEPTION_MESSAGE_TEMPLATE = "Сущность '{entity_name}' не найдена."

    def __init__(
        self,
        sqlalchemy_model: Base,
    ) -> None:
        detail = EntityNotFoundException.EXCEPTION_MESSAGE_TEMPLATE.format(
            entity_name=Base.metadata.tables[sqlalchemy_model.__tablename__].info["readable_name"]
        )
        super().__init__(404, detail)
