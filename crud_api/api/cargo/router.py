import uuid as uuid_pkg
from typing import Annotated

from api.cargo import schemas
from api.cargo.service import cargo_service
from database import get_db_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cargo", tags=["Грузы"])


@router.get("")
async def get_cargos(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[schemas.CargoWithId]:
    """
    Эндпойнт для получения всех грузов.

    Returns:
        list[schemas.CargoWithId]: Список грузов.
    """
    result: list[schemas.CargoWithId] = await cargo_service.get_objects(session)
    return result


@router.get("/{cargo_id}")
async def get_cargo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    cargo_id: uuid_pkg.UUID,
) -> schemas.CargoWithId:
    """
    Эндпойнт для получения конкретного груза.

    Args:
        cargo_id (uuid_pkg.UUID): Идентификатор груза.

    Returns:
        schemas.CargoWithId: Груз.
    """
    return await cargo_service.get_object(cargo_id, session)


@router.post("")
async def create_cargo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    cargo: schemas.CargoBase,
) -> schemas.CargoWithId:
    """
    Эндпойнт для создания груза.

    Args:
        cargo (schemas.CargoBase): Груз.

    Returns:
        schemas.CargoWithId: Груз.
    """
    return await cargo_service.create_object(
        cargo,
        session,
    )


@router.put("/{cargo_id}")
async def update_cargo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    cargo_id: uuid_pkg.UUID,
    cargo: schemas.CargoBase,
) -> schemas.CargoWithId:
    """
    Эндпойнт для обновления груза.

    Args:
        cargo_id (uuid_pkg.UUID): Идентификатор груза.
        cargo (schemas.CargoBase): Груз.

    Returns:
        schemas.CargoWithId: Груз.
    """
    return await cargo_service.update_object(
        cargo_id,
        cargo,
        session,
    )


@router.delete("/{cargo_id}")
async def delete_cargo(
    session: Annotated[AsyncSession, Depends(get_db_session)], cargo_id: uuid_pkg.UUID
) -> schemas.CargoWithId:
    """
    Эндпойнт для удаления груза.

    Args:
        cargo_id (uuid_pkg.UUID): Идентификатор груза.

    Returns:
        schemas.CargoWithId: Груз.
    """
    return await cargo_service.delete_object(cargo_id, session)
