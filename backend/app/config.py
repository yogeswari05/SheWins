from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    api_host: str = "0.0.0.0"
    # 8000 is often in Windows Hyper-V excluded port ranges → WinError 10013
    api_port: int = 8765
    cors_origins: str = "http://localhost:5173"

    firebase_credentials_path: str = ""  # env: FIREBASE_CREDENTIALS_PATH

    encryption_key: str = ""

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    jwt_secret: str = "dev-only-set-JWT_SECRET-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080  # 7 days

    groq_api_key: str = ""  # env: GROQ_API_KEY

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
