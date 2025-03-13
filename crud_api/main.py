# from api.router import router as api_router
from fastapi import FastAPI
# from observability.logging.middleware import enable_logging_middleware
# from observability.metrics import enable_metrics
# from settings import settings

app = FastAPI(
    title="CrudApi",
    version="1.0.0",
    contact={"name": "Maksim Omelchenko", "email": "omelchenko.ma@dns-shop.ru"},
)
