"""Flask error handler registration.

Translates application exceptions into JSON error responses. Registered once by
the application factory.
"""

from __future__ import annotations

from flask import Flask
from werkzeug.exceptions import HTTPException

from backend.shared.api_response import error
from backend.shared.errors import AppError


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def _handle_app_error(exc: AppError):
        return error(exc.error_code, exc.message, exc.status_code, exc.details)

    @app.errorhandler(HTTPException)
    def _handle_http_error(exc: HTTPException):
        code = (exc.name or "error").upper().replace(" ", "_")
        return error(code, exc.description or exc.name or "Error", exc.code or 500)
