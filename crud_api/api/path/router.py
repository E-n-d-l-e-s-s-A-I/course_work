import uuid as uuid_pkg
from typing import Annotated

from api.path import schemas
from api.path.service import path_service
from database import get_db_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/path", tags=["Пути"])


@router.get("")
async def get_paths(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[schemas.PathWithId]:
    """
    Эндпойнт для получения всех путей.

    Returns:
        list[schemas.PathWithId]: Список путей.
    """
    result: list[schemas.PathWithId] = await path_service.get_objects(session)
    return result


@router.get("/{path_id}")
async def get_path(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    path_id: uuid_pkg.UUID,
) -> schemas.PathWithId:
    """
    Эндпойнт для получения конкретного пути.

    Args:
        path_id (uuid_pkg.UUID): Идентификатор пути.

    Returns:
        schemas.PathWithId: Путь.
    """
    return await path_service.get_object(path_id, session)


@router.post("")
async def create_path(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    path: schemas.PathWithCities,
) -> schemas.PathWithId:
    """
    Эндпойнт для создания пути.

    Args:
        path (schemas.PathBase): Пути.

    Returns:
        schemas.PathWithId: Путь.
    """
    return await path_service.create_object(
        path,
        session,
    )


@router.put("/{path_id}")
async def update_path(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    path_id: uuid_pkg.UUID,
    path: schemas.PathBase,
) -> schemas.PathWithId:
    """
    Эндпойнт для обновления пути.

    Args:
        path_id (uuid_pkg.UUID): Идентификатор пути.
        path (schemas.CityBase): Путь.

    Returns:
        schemas.PathWithId: Путь.
    """
    return await path_service.update_object(
        path_id,
        path,
        session,
    )


@router.delete("/{path_id}")
async def delete_path(
    session: Annotated[AsyncSession, Depends(get_db_session)], path_id: uuid_pkg.UUID
) -> schemas.PathWithId:
    """
    Эндпойнт для удаления пути.

    Args:
        path_id (uuid_pkg.UUID): Идентификатор пути.

    Returns:
        schemas.PathWithId: Путь.
    """
    return await path_service.delete_object(path_id, session)
