from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
import os

class Settings(BaseSettings):
    """
    Central configuration for SignalMatrix Repo.
    Loads and validates environment variables from .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Required API Keys (will throw error if missing)
    github_token: str = Field(..., validation_alias="GITHUB_TOKEN")
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")

    # Optional Configuration
    openai_model: str = Field("gpt-4o-mini", validation_alias="OPENAI_MODEL")

# Singleton instance for globally accessible settings
settings = Settings()
