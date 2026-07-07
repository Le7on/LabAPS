"""Flask error handler registration.

Translates application exceptions into JSON error responses. Registered once by
the application factory.
"""

from __future__ import annotations

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from backend.shared.errors import AppError


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def _handle_app_error(exc: AppError):
        response = jsonify({"error": exc.error_code, "message": exc.message})
        response.status_code = exc.status_code
        return response

    @app.errorhandler(HTTPException)
    def _handle_http_error(exc: HTTPException):
        response = jsonify(
            {"error": exc.name.lower().replace(" ", "_"), "message": exc.description}
        )
        response.status_code = exc.code or 500
        return response
