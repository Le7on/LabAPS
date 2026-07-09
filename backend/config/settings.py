"""Application configuration loading.

Configuration is loaded once at startup and injected, never accessed globally
from business code (see Development Guide chapters 1 and 3).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv

CONFIG_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_FILE = CONFIG_DIR / "config.yaml"


@dataclass(slots=True)
class DatabaseConfig:
    url: str = "sqlite:///labaps.db"


@dataclass(slots=True)
class ApiConfig:
    prefix: str = "/api/v1"
    host: str = "127.0.0.1"
    port: int = 5000


@dataclass(slots=True)
class AppConfig:
    name: str = "Lab APS"
    version: str = "1.0.0"
    env: str = "development"
    auth_enabled: bool = True
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: ApiConfig = field(default_factory=ApiConfig)


def load_config(config_file: Path | None = None) -> AppConfig:
    """Load application configuration from YAML with environment overrides.

    Precedence (highest first): environment variables, YAML file, defaults.
    """

    load_dotenv()

    config = AppConfig()

    path = config_file or DEFAULT_CONFIG_FILE
    if path.is_file():
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        _apply_yaml(config, raw)

    _apply_env(config)

    return config


def _apply_yaml(config: AppConfig, raw: dict) -> None:
    app = raw.get("app", {})
    config.name = app.get("name", config.name)
    config.version = str(app.get("version", config.version))
    config.env = app.get("env", config.env)

    database = raw.get("database", {})
    config.database.url = database.get("url", config.database.url)

    api = raw.get("api", {})
    config.api.prefix = api.get("prefix", config.api.prefix)
    config.api.host = api.get("host", config.api.host)
    config.api.port = int(api.get("port", config.api.port))


def _apply_env(config: AppConfig) -> None:
    config.env = os.getenv("APP_ENV", config.env)
    config.database.url = os.getenv("DATABASE_URL", config.database.url)
    auth_env = os.getenv("AUTH_ENABLED")
    if auth_env is not None:
        config.auth_enabled = auth_env.strip().lower() not in ("0", "false", "no")
