import uuid as uuid_pkg
from typing import Annotated

from api.city import schemas
from api.city.service import city_service
from database import get_db_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/city", tags=["Города"])


@router.get("")
async def get_cities(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[schemas.CityWithId]:
    """
    Эндпойнт для получения всех городов.

    Returns:
        list[schemas.CityWithId]: Список городов.
    """
    result: list[schemas.CityWithId] = await city_service.get_objects(session)
    return result


@router.get("/{city_id}")
async def get_city(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    city_id: uuid_pkg.UUID,
) -> schemas.CityWithId:
    """
    Эндпойнт для получения конкретного города.

    Args:
        city_id (uuid_pkg.UUID): Идентификатор города.

    Returns:
        schemas.CityWithId: Город.
    """
    return await city_service.get_object(city_id, session)


@router.post("")
async def create_city(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    city: schemas.CityBase,
) -> schemas.CityWithId:
    """
    Эндпойнт для создания города.

    Args:
        city (schemas.CityBase): Город.

    Returns:
        schemas.CityWithId: Город.
    """
    return await city_service.create_object(
        city,
        session,
    )


@router.put("/{city_id}")
async def update_city(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    city_id: uuid_pkg.UUID,
    city: schemas.CityBase,
) -> schemas.CityWithId:
    """
    Эндпойнт для обновления города.

    Args:
        city_id (uuid_pkg.UUID): Идентификатор города.
        city (schemas.CityBase): Город.

    Returns:
        schemas.CityWithId: Город.
    """
    return await city_service.update_object(
        city_id,
        city,
        session,
    )


@router.delete("/{city_id}")
async def delete_city(
    session: Annotated[AsyncSession, Depends(get_db_session)], city_id: uuid_pkg.UUID
) -> schemas.CityWithId:
    """
    Эндпойнт для удаления города.

    Args:
        city_id (uuid_pkg.UUID): Идентификатор города.

    Returns:
        schemas.CityWithId: Город.
    """
    return await city_service.delete_object(city_id, session)
