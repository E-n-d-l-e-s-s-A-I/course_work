import uuid as uuid_pkg

import ops as ops
from api.cargo import schemas
from api.cargo.models import Cargo
from service import Service
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CargoService(Service):
    async def get_objects(
        self,
        session: AsyncSession,
    ) -> list[schemas.CargoWithId]:
        """
        Логика http-метода get для извлечения всех грузов.

        Args:
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Returns:
            list[schemas.CargoWithId]: Список грузов.
        """
        statement = select(Cargo)
        cargos: list[Cargo] = await ops.execute_to_get_many(statement, session)

        return [schemas.CargoWithId.model_validate(cargo) for cargo in cargos]

    async def get_object(
        self,
        cargo_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.CargoWithId:
        """
        Логика http-метода get для извлечения одного груза.

        Args:
            cargo_id (uuid_pkg.UUID): id груза.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            EntityNotFoundException: Груз не найдена.

        Returns:
            schemas.CargoWithId: Груз.
        """
        cargo = await ops.get_one_by_id(Cargo, cargo_id, session)
        return schemas.CargoWithId.model_validate(cargo)

    async def create_object(
        self,
        cargo: schemas.CargoBase,
        session: AsyncSession,
    ) -> schemas.CargoWithId:
        """
        Логика http-метода post для создания груза.

        Args:
            cargo (schemas.CargoBase): Pydantic схема груза.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Вставка нарушает целостность бд.

        Returns:
            schemas.CargoWithId: Груз.
        """

        cargo_sqlalchemy_object = await ops.create(
            Cargo,
            cargo.model_dump(),
            session,
        )
        return schemas.CargoWithId.model_validate(cargo_sqlalchemy_object)

    async def update_object(
        self,
        cargo_id: uuid_pkg.UUID,
        cargo: schemas.CargoBase,
        session: AsyncSession,
    ) -> schemas.CargoWithId:
        """
        Логика http-метода put для обновления груза.

        Args:
            cargo_id (uuid_pkg.UUID): id груза.
            cargo (schemas.CargoBase): Pydantic схема груза.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Обновление нарушает целостность бд.

        Returns:
            schemas.CargoWithId: Груз.
        """
        cargo_sqlalchemy_object = await ops.update(
            Cargo,
            cargo_id,
            cargo.model_dump(),
            session,
        )
        return schemas.CargoWithId.model_validate(cargo_sqlalchemy_object)

    async def delete_object(
        self,
        cargo_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.CargoWithId:
        """
        Логика http-метода delete для удаления груза.

        Args:
            cargo_id (uuid_pkg.UUID): id груза.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Удаление нарушает целостность бд.

        Returns:
            schemas.CargoWithId: Груз.
        """

        cargo = await ops.delete(Cargo, cargo_id, session)
        return schemas.CargoWithId.model_validate(cargo)


cargo_service = CargoService()
