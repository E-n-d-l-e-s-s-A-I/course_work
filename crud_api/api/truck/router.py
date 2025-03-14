import uuid as uuid_pkg
from typing import Annotated

from api.truck import schemas
from api.truck.service import truck_service
from database import get_db_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/truck", tags=["Грузовики"])


@router.get("")
async def get_trucks(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[schemas.TruckWithId]:
    """
    Эндпойнт для получения всех грузовиков.

    Returns:
        list[schemas.TruckWithId]: Список грузовиков.
    """
    result: list[schemas.TruckWithId] = await truck_service.get_objects(session)
    return result


@router.get("/{truck_id}")
async def get_truck(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    truck_id: uuid_pkg.UUID,
) -> schemas.TruckWithId:
    """
    Эндпойнт для получения конкретного грузовика.

    Args:
        truck_id (uuid_pkg.UUID): Идентификатор грузовика.

    Returns:
        schemas.TruckWithId: Грузовик.
    """
    return await truck_service.get_object(truck_id, session)


@router.post("")
async def create_truck(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    truck: schemas.TruckBase,
) -> schemas.TruckWithId:
    """
    Эндпойнт для создания грузовика.

    Args:
        truck (schemas.TruckBase): Грузовик.

    Returns:
        schemas.TruckWithId: Грузовик.
    """
    return await truck_service.create_object(
        truck,
        session,
    )


@router.put("/{truck_id}")
async def update_truck(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    truck_id: uuid_pkg.UUID,
    truck: schemas.TruckBase,
) -> schemas.TruckWithId:
    """
    Эндпойнт для обновления грузовика.

    Args:
        truck_id (uuid_pkg.UUID): Идентификатор грузовика.
        truck (schemas.TruckBase): Грузовик.

    Returns:
        schemas.TruckWithId: Грузовик.
    """
    return await truck_service.update_object(
        truck_id,
        truck,
        session,
    )


@router.delete("/{truck_id}")
async def delete_truck(
    session: Annotated[AsyncSession, Depends(get_db_session)], truck_id: uuid_pkg.UUID
) -> schemas.TruckWithId:
    """
    Эндпойнт для удаления грузовика.

    Args:
        truck_id (uuid_pkg.UUID): Идентификатор грузовика.

    Returns:
        schemas.TruckWithId: Грузовик.
    """
    return await truck_service.delete_object(truck_id, session)
