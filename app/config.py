from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Blockstak News API"
    API_PREFIX: str = "/api/v1"
    
    # Security settings
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./news.db"
    
    # NewsAPI settings
    NEWSAPI_KEY: str
    NEWSAPI_BASE_URL: str = "https://newsapi.org/v2"
    
    # Auth client settings
    CLIENT_ID: str = "blockstak_client"
    CLIENT_SECRET: str = "blockstak_secret"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()