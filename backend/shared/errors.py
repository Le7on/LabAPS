"""Shared application exceptions.

Cross-cutting error types used across modules. These carry an HTTP status so the
API layer can translate them into responses without leaking framework types into
the domain.
"""

from __future__ import annotations


class AppError(Exception):
    """Base application error.

    Carries a stable SCREAMING_SNAKE ``error_code`` (independent of UI wording),
    an HTTP ``status_code``, and optional per-field ``details`` (ADR-012).
    """

    status_code = 500
    error_code = "INTERNAL_ERROR"

    def __init__(self, message: str | None = None, details: list | None = None):
        super().__init__(message or self.__class__.__name__)
        self.message = message or self.__class__.__name__
        self.details = details or []


class ValidationError(AppError):
    """Request or domain validation failed (HTTP 422)."""

    status_code = 422
    error_code = "VALIDATION_FAILED"


class NotFoundError(AppError):
    """A requested resource does not exist (HTTP 404)."""

    status_code = 404
    error_code = "NOT_FOUND"


class ConflictError(AppError):
    """The request conflicts with the current state of a resource (HTTP 409)."""

    status_code = 409
    error_code = "CONFLICT"


class UnauthorizedError(AppError):
    """Authentication is missing or invalid (HTTP 401)."""

    status_code = 401
    error_code = "UNAUTHORIZED"


class ForbiddenError(AppError):
    """The authenticated user lacks the required role (HTTP 403)."""

    status_code = 403
    error_code = "FORBIDDEN"
