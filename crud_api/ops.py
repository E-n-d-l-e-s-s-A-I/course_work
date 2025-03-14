from collections.abc import Sequence
from typing import Any, TypeVar
from uuid import UUID

from exceptions import DBIntegrityException, EntityNotFoundException
from models import Base
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable

TSqlalhemyModel = TypeVar("TSqlalhemyModel", bound=Base)


async def get_one_by_id(
    sqlalchemy_model: type[TSqlalhemyModel],
    id_: UUID | str,
    session: AsyncSession,
) -> TSqlalhemyModel:
    """
    Вспомогательная функция для извлечения объекта из бд по id.

    Args:
        sqlalchemy_model (type[TSqlalhemyModel]): Sqlalchemy модель, объект которой нужно извлечь.
        id_: Union[UUID, str]: id объекта.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.

    Raises:
        EntityNotFoundException: Объект не найден.

    Returns:
        TSqlalhemyModel: Извлеченный sqlalchemy объект.
    """
    sqlalchemy_object: TSqlalhemyModel | None = await session.get(sqlalchemy_model, str(id_))

    if not sqlalchemy_object:
        raise EntityNotFoundException(sqlalchemy_model)

    return sqlalchemy_object


async def execute_to_get_many(
    statement: Executable,
    session: AsyncSession,
) -> Sequence[TSqlalhemyModel]:
    """
    Вспомогательная функция для выполнения запроса на извлечение нескольких объектов из бд.

    Args:
        statement (Executable): Sqlalchemy выражение для извлечения объектов.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.

    Returns:
        Sequence[TSqlalhemyModel]: Извлеченные sqlalchemy объекты.
    """
    response = await session.execute(statement)
    sqlalchemy_objects: Sequence[TSqlalhemyModel] = response.scalars().unique().all()
    return sqlalchemy_objects


async def execute_to_get_one(
    statement: Executable,
    sqlalchemy_model: type[TSqlalhemyModel],
    session: AsyncSession,
) -> TSqlalhemyModel:
    """
    Вспомогательная функция для выполнения запроса на извлечение одного объекта из бд.

    Args:
        statement (Executable): Sqlalchemy выражение для извлечения объекта.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.

    Raises:
        EntityNotFoundException: Объект не найден.

    Returns:
        TSqlalhemyModel: Извлеченный sqlalchemy объект.
    """
    response = await session.execute(statement)
    sqlalchemy_object: TSqlalhemyModel | None = response.unique().scalar_one_or_none()
    if not sqlalchemy_object:
        raise EntityNotFoundException(sqlalchemy_model)

    return sqlalchemy_object


async def create(
    sqlalchemy_model: type[TSqlalhemyModel],
    row_data: dict[str, Any],
    session: AsyncSession,
    with_commit: bool = True,
) -> TSqlalhemyModel:
    """
    Вспомогательная функция для создания объекта в бд.

    Args:
        sqlalchemy_model (type[TSqlalhemyModel]): Sqlalchemy модель, объект которой нужно создать.
        row_data: dict[str, Any]: Сырые данные по которым нужно создать объект.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.
        with_commit (bool): Совершить добавление принудительно сразу с коммитом.

    Raises:
        DBIntegrityException: Вставка нарушает целостность бд.

    Returns:
        TSqlalhemyModel: созданный sqlalchemy объект.
    """
    sqlalchemy_object: TSqlalhemyModel = sqlalchemy_model(**row_data)

    session.add(sqlalchemy_object)
    if with_commit:
        return await refresh_object(sqlalchemy_object, session)
    return sqlalchemy_object


async def update(
    sqlalchemy_model: type[TSqlalhemyModel],
    id_: UUID | str,
    row_data: dict[str, Any],
    session: AsyncSession,
    with_commit: bool = True,
) -> TSqlalhemyModel:
    """
    Вспомогательная функция для обновления объекта в бд.

    Args:
        sqlalchemy_model (type[TSqlalhemyModel]): Sqlalchemy модель, объект которой нужно обновить.
        id_ (Union[UUID, str]): id, объекта, который нужно обновить.
        row_data: dict[str, Any]:Сырые данные по которым нужно обновить объект.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.

    Raises:
        DBIntegrityException: Обновление нарушает целостность бд.

    Returns:
        TSqlalhemyModel: созданный sqlalchemy объект.
    """
    sqlalchemy_object = await get_one_by_id(sqlalchemy_model, id_, session)
    for key, value in row_data.items():
        setattr(sqlalchemy_object, key, value)
    if with_commit:
        return await refresh_object(sqlalchemy_object, session)
    return sqlalchemy_object


async def delete(
    sqlalchemy_model: type[TSqlalhemyModel],
    id_: UUID | str,
    session: AsyncSession,
) -> TSqlalhemyModel:
    """
    Вспомогательная функция для удаления объекта в бд.

    Args:
        sqlalchemy_model (type[TSqlalhemyModel]): Sqlalchemy модель, объект которой нужно удалить.
        id_ (Union[UUID, str]): id, объекта, который нужно удалить.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.

    Raises:
        DBIntegrityException: Удаление нарушает целостность бд.

    Returns:
        TSqlalhemyModel: удаленный sqlalchemy объект.
    """
    sqlalchemy_object = await get_one_by_id(sqlalchemy_model, id_, session)
    await session.delete(sqlalchemy_object)
    try:
        await session.commit()
        return sqlalchemy_object
    except IntegrityError as e:
        await session.rollback()
        raise DBIntegrityException(detail=str(e)) from e


async def refresh_object(
    sqlalchemy_object: TSqlalhemyModel,
    session: AsyncSession,
) -> TSqlalhemyModel:
    """
    Обновляет аттрибуты объекта по данным из бд.

    Args:
        sqlalchemy_object (TSqlalhemyModel): Объект который нужно обновить.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.

    Raises:
        DBIntegrityException: Обновление нарушает целостность бд.

    Returns:
        TSqlalhemyModel: Обновленный объект.
    """
    try:
        await session.commit()
        await session.refresh(sqlalchemy_object)
        return sqlalchemy_object
    except IntegrityError as e:
        await session.rollback()
        raise DBIntegrityException(detail=str(e)) from e


async def count(
    sqlalchemy_model: type[TSqlalhemyModel],
    session: AsyncSession,
) -> int:
    """
    Вспомогательная функция для получения количества объектов в бд.

    Args:
        sqlalchemy_model (type[TSqlalhemyModel]): Sqlalchemy модель, объект которой нужно обновить.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.

    Returns:
        TSqlalhemyModel: созданный sqlalchemy объект.
    """
    statement = select(func.count()).select_from(sqlalchemy_model)
    result = await session.execute(statement)
    objects_count = result.scalar() or 0

    return objects_count
