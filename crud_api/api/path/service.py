import uuid as uuid_pkg

import ops as ops
from api.path import schemas
from api.path.models import Path
from fastapi import HTTPException
from service import Service
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PathService(Service):
    async def get_objects(
        self,
        session: AsyncSession,
    ) -> list[schemas.PathWithId]:
        """
        Логика http-метода get для извлечения всех путей.

        Args:
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Returns:
            list[schemas.PathWithId]: Список путей.
        """
        statement = select(Path)
        paths: list[Path] = await ops.execute_to_get_many(statement, session)

        return [schemas.PathWithId.model_validate(path) for path in paths]

    async def get_object(
        self,
        path_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.PathWithId:
        """
        Логика http-метода get для извлечения одного пути.

        Args:
            path_id (uuid_pkg.UUID): id пути.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            EntityNotFoundException: Путь не найдена.

        Returns:
            schemas.PathWithId: Путь.
        """
        path = await ops.get_one_by_id(Path, path_id, session)
        return schemas.PathWithId.model_validate(path)

    async def create_object(
        self,
        path: schemas.PathBase,
        session: AsyncSession,
    ) -> schemas.PathWithId:
        """
        Логика http-метода post для создания пути.

        Args:
            path (schemas.PathBase): Pydantic схема пути.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Вставка нарушает целостность бд.

        Returns:
            schemas.PathWithId: Путь.
        """
        await self.check_path_not_exist(path, session)

        path_sqlalchemy_object = await ops.create(
            Path,
            path.model_dump(),
            session,
        )
        return schemas.PathWithId.model_validate(path_sqlalchemy_object)

    async def update_object(
        self,
        path_id: uuid_pkg.UUID,
        path: schemas.PathBase,
        session: AsyncSession,
    ) -> schemas.PathWithId:
        """
        Логика http-метода put для обновления пути.

        Args:
            path_id (uuid_pkg.UUID): id пути.
            path (schemas.PathBase): Pydantic схема пути.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Обновление нарушает целостность бд.

        Returns:
            schemas.PathWithId: Путь.
        """
        await self.check_path_not_exist(path, session)

        path_sqlalchemy_object = await ops.update(
            Path,
            path_id,
            path.model_dump(),
            session,
        )
        return schemas.PathWithId.model_validate(path_sqlalchemy_object)

    async def delete_object(
        self,
        path_id: uuid_pkg.UUID,
        session: AsyncSession,
    ) -> schemas.PathWithId:
        """
        Логика http-метода delete для удаления пути.

        Args:
            path_id (uuid_pkg.UUID): id пути.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            DBIntegrityException: Удаление нарушает целостность бд.

        Returns:
            schemas.PathWithId: Путь.
        """

        path = await ops.delete(Path, path_id, session)
        return schemas.PathWithId.model_validate(path)

    async def check_path_not_exist(self, path: schemas.PathBase, session: AsyncSession):
        """
        Проверяет, что путь не существует в базе.

        Args:
            path (schemas.PathBase): Путь.
            session (AsyncSession): Асинхронная Sqlalchemy сессия.

        Raises:
            HTTPException: 409, если путь существует.
        """
        statement = select(Path)

        # Находим множество существующий путей, сортируем пути чтобы учесть,
        # что путь (a, b) = (b, a) и бд может быть только один из них
        paths: list[Path] = await ops.execute_to_get_many(statement, session)
        city_pairs = set(tuple(sorted([path.city_from_id, path.city_to_id])) for path in paths)

        new_pair = tuple(sorted([path.city_from_id, path.city_to_id]))

        if new_pair in city_pairs:
            raise HTTPException(409, "Путь уже существует")


path_service = PathService()
