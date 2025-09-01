"""
Application configuration settings.

This module contains the application configuration
settings using Pydantic Settings.
"""

from typing import Any, List, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv("/Users/yosifelessawi/Desktop/FastAPI/.env")


class Settings(BaseSettings):
    # Application Settings
    DEBUG: bool = False
    PROJECT_NAME: str = "FastAPI Todo App"
    VERSION: str = "1.0.0"

    # API Settings
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # JWT Settings
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 8 days

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Return the async database URL."""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return self.DATABASE_URL

    # CORS
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",  # Common frontend dev port
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
    ]

    # First Superuser
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
        if field_name == "BACKEND_CORS_ORIGINS" and raw_val:
            if isinstance(raw_val, str) and not raw_val.startswith("["):
                return [i.strip() for i in raw_val.split(",")]
            elif isinstance(raw_val, list):
                return raw_val
        return cls.model_validate_json(raw_val)


# Create settings instance
settings = Settings()
