"""Application Factory.

Creates the Flask runtime environment. Assembles configuration, logging, the
dependency container, error handlers and API blueprints. Contains no business
logic (see Development Guide chapters 1-3).
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, send_from_directory

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

    # Development/test convenience: ensure schema exists. Production schema
    # changes are managed through Alembic migrations.
    container.database.create_all()

    register_error_handlers(app)

    if app_config.auth_enabled:
        from backend.shared.auth import register_auth_guard

        register_auth_guard(app, container.auth_service, app_config.api.prefix)

    register_blueprints(app, container)
    register_frontend(app)

    return app


def register_frontend(app: Flask) -> None:
    """Serve the built SPA (frontend/dist) when present, for desktop packaging.

    In development the SPA is served by Vite; in a packaged desktop build the
    Flask app serves the static bundle and falls back to index.html for client
    routes. No-op if the build is absent.
    """

    dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
    index = dist / "index.html"
    if not index.is_file():
        return

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def _serve_spa(path: str):
        # API paths are handled by blueprints; never serve the SPA for them.
        if path.startswith("api/"):
            from werkzeug.exceptions import NotFound

            raise NotFound()
        target = dist / path
        if path and target.is_file():
            return send_from_directory(dist, path)
        return send_from_directory(dist, "index.html")


def register_blueprints(app: Flask, container: Container) -> None:
    """Register module API blueprints under the configured prefix."""

    prefix = container.config.api.prefix

    from backend.modules.execution.api.executions_api import executions_bp
    from backend.modules.identity.api.auth_api import auth_bp
    from backend.modules.laboratory.api.equipment_api import equipment_bp
    from backend.modules.laboratory.api.project_api import project_bp
    from backend.modules.laboratory.api.staff_api import staff_bp
    from backend.modules.laboratory.api.workflow_definition_api import (
        workflow_definition_bp,
    )
    from backend.modules.planning.api.plans_api import plans_bp
    from backend.modules.reporting.api.dashboard_api import dashboard_bp
    from backend.shared.health import health_bp

    app.register_blueprint(health_bp, url_prefix=prefix)
    app.register_blueprint(plans_bp, url_prefix=prefix)
    app.register_blueprint(equipment_bp, url_prefix=prefix)
    app.register_blueprint(staff_bp, url_prefix=prefix)
    app.register_blueprint(project_bp, url_prefix=prefix)
    app.register_blueprint(workflow_definition_bp, url_prefix=prefix)
    app.register_blueprint(dashboard_bp, url_prefix=prefix)
    app.register_blueprint(executions_bp, url_prefix=prefix)
    app.register_blueprint(auth_bp, url_prefix=prefix)
