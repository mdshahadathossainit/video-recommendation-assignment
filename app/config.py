# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from functools import lru_cache # Added for caching

class Settings(BaseSettings):
    # Your provided variables are here
    YOUTUBE_API_KEY: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    DATABASE_URL: str = "sqlite+aiosqlite:///app/db/dev.db"
    FLIC_TOKEN: str = ""
    PAGE_SIZE: int = 20
    API_BASE_URL: AnyUrl # Base URL for the YouTube API

    # pydantic-settings v2.x configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    This function is required by other modules (like recommender.py)
    to access configuration settings without repeatedly loading .env.
    """
    return Settings()

# Instance of settings for direct application-level use
settings = get_settings()