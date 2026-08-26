"""
Application Configuration
========================
Uses Pydantic Settings to load configuration from environment variables.
All settings have sensible defaults for local development.

Learn more:
- Pydantic Settings docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- 12-Factor App config: https://12factor.net/config
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Pydantic Settings automatically reads from:
    1. Environment variables
    2. .env file (if python-dotenv is installed)
    3. Default values defined here
    
    Priority: env vars > .env file > defaults
    """

    # ---- Application ----
    APP_NAME: str = "Palmistry & Tarot Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # ---- Server ----
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ---- Security ----
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ---- PostgreSQL ----
    DATABASE_URL: str = "postgresql+asyncpg://admin:secret123@localhost:5432/palmistry_tarot"

    # ---- MongoDB ----
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "palmistry_tarot"

    # ---- Redis ----
    REDIS_URL: str = "redis://localhost:6379/0"

    # ---- Google OAuth2 ----
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # ---- CORS ----
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a global settings instance
# This is imported throughout the app: from app.config import settings
settings = Settings()
