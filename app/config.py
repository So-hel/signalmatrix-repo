from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import Optional
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

    # API Keys
    github_token: str = Field(..., validation_alias="GITHUB_TOKEN")
    openai_api_key: Optional[str] = Field(None, validation_alias="OPENAI_API_KEY")
    blackbox_api_key: Optional[str] = Field(None, validation_alias="BLACKBOX_API_KEY")

    # AI Configuration
    ai_provider: str = Field("openai", validation_alias="AI_PROVIDER") # 'openai' or 'blackbox'
    openai_model: str = Field("gpt-4o-mini", validation_alias="OPENAI_MODEL")
    blackbox_model: str = Field("blackboxai", validation_alias="BLACKBOX_MODEL")

# Singleton instance for globally accessible settings
settings = Settings()
