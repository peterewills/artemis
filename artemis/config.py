import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Required environment variables
    anthropic_api_key: str
    
    # API Security
    api_key: str | None = None  # Optional API key for authentication

    # Model settings
    model_name: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 0.7

    # API settings - Railway automatically sets PORT
    api_host: str = "0.0.0.0"
    api_port: int = int(
        os.getenv("PORT", 8000)
    )  # Railway sets PORT, fallback to 8000 for local

    class Config:
        env_file = None  # Don't look for .env file


settings = Settings()
