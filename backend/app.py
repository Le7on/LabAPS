"""Application Factory.

Creates the Flask runtime environment. Assembles configuration, logging, the
dependency container, error handlers and API blueprints. Contains no business
logic (see Development Guide chapters 1-3).
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask

from backend.bootstrap.container import Container, build_container
from backend.bootstrap.logging_setup import init_logging
from backend.config.settings import AppConfig, load_config
from backend.shared.error_handlers import register_error_handlers


def create_app(config: AppConfig | None = None, config_file: Path | None = None) -> Flask:
    """Create and configure the Flask application.

    Steps mirror the documented startup sequence: load configuration, initialize
    logging, build the composition root, register error handlers, register the
    REST API.
    """

    init_logging()

    app_config = config or load_config(config_file)

    app = Flask(__name__)
    app.config["APP_CONFIG"] = app_config

    container = build_container(app_config)
    app.config["CONTAINER"] = container

    register_error_handlers(app)
    register_blueprints(app, container)

    return app


def register_blueprints(app: Flask, container: Container) -> None:
    """Register module API blueprints under the configured prefix."""

    prefix = container.config.api.prefix

    from backend.shared.health import health_bp

    app.register_blueprint(health_bp, url_prefix=prefix)
