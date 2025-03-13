# from api.router import router as api_router
from typing import Annotated
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_db_session


app = FastAPI(
    title="CrudApi",
    version="1.0.0",
    contact={"name": "Maksim Omelchenko", "email": "omelchenko.ma@dns-shop.ru"},
)


@app.post("/add_city")
async def create_model(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> str:
    """Тестовый эндпоинт чтобы проверить подключение к бд."""
    import random
    from api.city.models import City

    city_names = ["Москва", "Владивосток"]
    city = City(name=random.choice(city_names))

    session.add(city)
    await session.commit()
    await session.refresh(city)
    return str(city.id)
