from api.router import router as api_router
from fastapi import FastAPI

app = FastAPI(
    title="CrudApi",
    version="1.0.0",
    contact={"name": "Maksim Omelchenko", "email": "omelchenko.ma@dns-shop.ru"},
)
app.include_router(api_router)
