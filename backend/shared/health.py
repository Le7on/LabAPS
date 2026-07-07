"""Health check endpoint.

A minimal blueprint that proves the REST API is assembled and reachable. Carries
no business logic.
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    config = current_app.config["APP_CONFIG"]
    return jsonify(
        {
            "status": "ok",
            "app": config.name,
            "version": config.version,
            "env": config.env,
        }
    )
