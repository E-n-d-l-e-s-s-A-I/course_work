import uuid as uuid_pkg

import ops as ops
from api.city import schemas
from api.city.models import City
from service import Service
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CityService(Service):
    async def get_objects(
        self,
        session: AsyncSession,
    ) -> list[schemas.CityWithId]:
        """
        Логика http-метода get для извлечения всех городов.

        Args:
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Returns:
            list[schemas.CityWithId]: Список городов.
        """
        statement = select(City)
        cities: list[City] = await ops.execute_to_get_many(statement, session)

        return [schemas.CityWithId.model_validate(city) for city in cities]

    async def get_object(
        self,
        city_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.CityWithId:
        """
        Логика http-метода get для извлечения одного города.

        Args:
            city_id (uuid_pkg.UUID): id города.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            EntityNotFoundException: Город не найдена.

        Returns:
            schemas.CityWithId: Город.
        """
        city = await ops.get_one_by_id(City, city_id, session)
        return schemas.CityWithId.model_validate(city)

    async def create_object(
        self,
        city: schemas.CityBase,
        session: AsyncSession,
    ) -> schemas.CityWithId:
        """
        Логика http-метода post для создания города.

        Args:
            city (schemas.CityBase): Pydantic схема города.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Вставка нарушает целостность бд.

        Returns:
            schemas.CityWithId: Город.
        """

        city_sqlalchemy_object = await ops.create(
            City,
            city.model_dump(),
            session,
        )
        return schemas.CityWithId.model_validate(city_sqlalchemy_object)

    async def update_object(
        self,
        city_id: uuid_pkg.UUID,
        city: schemas.CityBase,
        session: AsyncSession,
    ) -> schemas.CityWithId:
        """
        Логика http-метода put для обновления города.

        Args:
            city_id (uuid_pkg.UUID): id города.
            city (schemas.CityBase): Pydantic схема города.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Обновление нарушает целостность бд.

        Returns:
            schemas.CityWithId: Город.
        """
        city_sqlalchemy_object = await ops.update(
            City,
            city_id,
            city.model_dump(),
            session,
        )
        return schemas.CityWithId.model_validate(city_sqlalchemy_object)

    async def delete_object(
        self,
        city_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.CityWithId:
        """
        Логика http-метода delete для удаления города.

        Args:
            city_id (uuid_pkg.UUID): id города.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Удаление нарушает целостность бд.

        Returns:
            schemas.CityWithId: Город.
        """

        city = await ops.delete(City, city_id, session)
        return schemas.CityWithId.model_validate(city)


city_service = CityService()
