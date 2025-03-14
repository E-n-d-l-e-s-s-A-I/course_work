from collections.abc import AsyncGenerator

from settings import settings
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    settings.database.metadata_uri,
    future=True,
)

async_session_factory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator:
    """
    Функция, возвращающая асинхронную сессия с бд.

    Yields:
        Iterator[AsyncGenerator]: асинхронную сессия с бд.
    """
    async with async_session_factory() as session:
        yield session


class Base(DeclarativeBase):
    """Базовый класс orm таблиц."""
