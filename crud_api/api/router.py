from api.cargo.router import router as cargo_router
from api.city.router import router as city_router
from api.truck.router import router as truck_router
from fastapi import APIRouter

router = APIRouter()
routers_to_include = [city_router, cargo_router, truck_router]
[router.include_router(router_to_include) for router_to_include in routers_to_include]
