from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    YOUTUBE_API_KEY: str = Field(..., description="Your YouTube Data API v3 key.")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

def get_settings():
    return Settings()
