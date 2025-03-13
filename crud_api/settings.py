from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """Конфиг для базы данных."""

    metadata_uri: str


class Settings(BaseSettings):
    """Глобальный конфиг."""

    database: DatabaseSettings

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings(_env_file="../.env", _env_nested_delimiter="__")
