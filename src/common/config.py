from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import Optional


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: Optional[bool] = False
    API_VERSION: Optional[str] = None
    # AWS environment variable
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None

    # Dynamically set env_file based on ENVIRONMENT environment variable
    model_config = SettingsConfigDict(
        env_file=(
            f"config/env/python-template-service.{os.getenv('ENVIRONMENT', 'development')}.env",
            "config/secrets/secret-python-template-service.env",
        ),
        extra="allow",  # <-- allow extra env vars without validation error
    )


settings = Settings()
