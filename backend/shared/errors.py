"""Shared application exceptions.

Cross-cutting error types used across modules. These carry an HTTP status so the
API layer can translate them into responses without leaking framework types into
the domain.
"""

from __future__ import annotations


class AppError(Exception):
    """Base application error."""

    status_code = 500
    error_code = "internal_error"

    def __init__(self, message: str | None = None):
        super().__init__(message or self.__class__.__name__)
        self.message = message or self.__class__.__name__


class ValidationError(AppError):
    """Request or domain validation failed."""

    status_code = 400
    error_code = "validation_error"


class NotFoundError(AppError):
    """A requested resource does not exist."""

    status_code = 404
    error_code = "not_found"


class ConflictError(AppError):
    """The request conflicts with the current state of a resource."""

    status_code = 409
    error_code = "conflict"
