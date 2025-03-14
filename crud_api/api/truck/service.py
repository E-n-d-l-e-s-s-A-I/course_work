import uuid as uuid_pkg

import ops as ops
from api.truck import schemas
from api.truck.models import Truck
from service import Service
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TruckService(Service):
    async def get_objects(
        self,
        session: AsyncSession,
    ) -> list[schemas.TruckWithId]:
        """
        Логика http-метода get для извлечения всех грузовиков.

        Args:
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Returns:
            list[schemas.TruckWithId]: Список грузовиков.
        """
        statement = select(Truck)
        trucks: list[Truck] = await ops.execute_to_get_many(statement, session)

        return [schemas.TruckWithId.model_validate(truck) for truck in trucks]

    async def get_object(
        self,
        truck_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.TruckWithId:
        """
        Логика http-метода get для извлечения одного грузовика.

        Args:
            truck_id (uuid_pkg.UUID): id грузовика.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            EntityNotFoundException: Грузовик не найдена.

        Returns:
            schemas.TruckWithId: Грузовик.
        """
        truck = await ops.get_one_by_id(Truck, truck_id, session)
        return schemas.TruckWithId.model_validate(truck)

    async def create_object(
        self,
        truck: schemas.TruckBase,
        session: AsyncSession,
    ) -> schemas.TruckWithId:
        """
        Логика http-метода post для создания грузовика.

        Args:
            truck (schemas.TruckBase): Pydantic схема грузовика.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Вставка нарушает целостность бд.

        Returns:
            schemas.TruckWithId: Грузовик.
        """

        truck_sqlalchemy_object = await ops.create(
            Truck,
            truck.model_dump(),
            session,
        )
        return schemas.TruckWithId.model_validate(truck_sqlalchemy_object)

    async def update_object(
        self,
        truck_id: uuid_pkg.UUID,
        truck: schemas.TruckBase,
        session: AsyncSession,
    ) -> schemas.TruckWithId:
        """
        Логика http-метода put для обновления грузовика.

        Args:
            truck_id (uuid_pkg.UUID): id грузовика.
            truck (schemas.TruckBase): Pydantic схема грузовика.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Обновление нарушает целостность бд.

        Returns:
            schemas.TruckWithId: Грузовик.
        """
        truck_sqlalchemy_object = await ops.update(
            Truck,
            truck_id,
            truck.model_dump(),
            session,
        )
        return schemas.TruckWithId.model_validate(truck_sqlalchemy_object)

    async def delete_object(
        self,
        truck_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.TruckWithId:
        """
        Логика http-метода delete для удаления грузовика.

        Args:
            truck_id (uuid_pkg.UUID): id грузовика.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Удаление нарушает целостность бд.

        Returns:
            schemas.TruckWithId: Грузовик.
        """

        truck = await ops.delete(Truck, truck_id, session)
        return schemas.TruckWithId.model_validate(truck)


truck_service = TruckService()
