from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ForgeOps AI Engineering Platform"
    environment: str = "local"
    database_url: str = "sqlite+aiosqlite:///./forgeops.db"
    jwt_secret: str = "LOCAL-ONLY-CHANGE-ME-BEFORE-ANY-NONLOCAL-USE"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
