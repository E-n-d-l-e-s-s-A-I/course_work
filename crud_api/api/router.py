from api.city.router import router as city_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(city_router)
