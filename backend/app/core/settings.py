from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All config comes from the environment (or backend/.env in dev)."""

    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")

    database_url: str = "postgresql+psycopg://app:app@127.0.0.1:5432/app"
    redis_url: str = "redis://127.0.0.1:6379/0"
    llm_model: str = "test"
    app_name: str = "myapp"
    api_port: int = 8000
    db_null_pool: bool = False  # tests: no pooled connections across event loops


@lru_cache
def get_settings() -> Settings:
    return Settings()
