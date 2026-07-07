"""Health check endpoint.

A minimal blueprint that proves the REST API is assembled and reachable. Carries
no business logic.
"""

from __future__ import annotations

from flask import Blueprint, current_app

from backend.shared import api_response

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    config = current_app.config["APP_CONFIG"]
    return api_response.success(
        {
            "status": "ok",
            "app": config.name,
            "version": config.version,
            "env": config.env,
        }
    )
