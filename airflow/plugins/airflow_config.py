from functools import cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

_base_dir = Path(__file__).parent


class AppConfig(BaseSettings):
    environment: Literal["dev", "prod"]

    @property
    def base_dir(self) -> Path:
        return _base_dir


class OpenAPIConfig(BaseSettings):
    project: str
    secret: str


class ApplicationBackendConfig(BaseSettings):
    url: str
    token: str


class Settings(BaseSettings):
    app: AppConfig
    application_backend: ApplicationBackendConfig
    open_ai: OpenAPIConfig

    model_config = SettingsConfigDict(
        env_prefix="AIRFLOW_VAR_",
        env_nested_delimiter="__",
    )


@cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
