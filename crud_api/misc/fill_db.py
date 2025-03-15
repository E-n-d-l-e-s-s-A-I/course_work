import json
import logging
import os

import database as database
from models import (
    Base,
    Cargo,
    City,
    Path,
    Truck,
)
from settings import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

PATH_TO_SAMPLES_DIR = "/samples"


MODELS_TO_LOAD: tuple[type[Base], ...] = (
    Truck,
    Cargo,
    City,
    Path,
)  # модели которые будут загружены командой fill_test_data


def load_data(sample_path: str, model: type[Base], session: AsyncSession) -> None:
    """
    Загружает данные в бд из json-файла.

    Args:
        sample_path (str): путь к json-файлу.
        model (type[TSqlalhemyModel]): Sqlalchemy модель в которую нужно вставить данные.
        session (AsyncSession): Асинхронная Sqlalchemy сессия.
    """
    with open(sample_path) as file:
        samples = json.load(file)
        for sample in samples:
            sample = model(**sample)
            session.add(sample)


async def fill_db(models: tuple[type[Base], ...]) -> None:
    """
    Заполняет бд тестовыми данными.

    Args:
        models (list[type[TSqlalhemyModel]]):
        список sqlalchemy моделей, в которые нужно залить тестовые данные.
    """
    entities_to_load = [
        (model, os.getcwd() + f"{PATH_TO_SAMPLES_DIR}/{model.__tablename__}.json")
        for model in models
    ]
    engine = create_async_engine(
        settings.database.metadata_uri,
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        async_session_factory = async_sessionmaker(engine, autoflush=False)

        async with async_session_factory() as session:
            for entity_to_load in entities_to_load:
                model, sample_path = entity_to_load
                response = await session.execute(text(f"select * from {model.__tablename__}"))
                sqlalchemy_obj = response.fetchone()
                if not sqlalchemy_obj:
                    logging.info(f"Объект {model.__name__} не залит. Заливаем данные...")
                    load_data(sample_path, model, session)
                    await session.commit()
                else:
                    logging.info(f"Объект {model.__name__} уже залит.")

            await session.commit()


async def fill_test_data() -> None:
    """Функция для заполнения бд тестовыми данными. Вызывается cli."""
    logging.info("Запускаем заливку данных в тестовую БД...")
    await fill_db(MODELS_TO_LOAD)
