"""Authentication guard and role authorization (ADR-013).

A single before_request guard resolves the bearer token to the current user and
stores it on ``flask.g``. Public paths (health) are exempt. A ``require_role``
decorator enforces authorization at the endpoint. Auth failures use the standard
error envelope via the shared exceptions.
"""

from __future__ import annotations

import functools

from flask import Flask, g, request

from backend.modules.identity.domain.role import Role
from backend.shared.errors import ForbiddenError, UnauthorizedError

# Path suffixes that do not require authentication.
_PUBLIC_SUFFIXES = ("/health",)


def register_auth_guard(app: Flask, auth_service) -> None:
    @app.before_request
    def _authenticate():
        if request.method == "OPTIONS":
            return
        path = request.path
        if any(path.endswith(suffix) for suffix in _PUBLIC_SUFFIXES):
            return

        header = request.headers.get("Authorization", "")
        token = header[7:] if header.startswith("Bearer ") else ""
        user = auth_service.resolve(token)
        if user is None:
            raise UnauthorizedError("Valid authentication token required")
        g.current_user = user


def current_user():
    return getattr(g, "current_user", None)


def require_role(*roles: Role):
    """Endpoint decorator enforcing that the current user has one of ``roles``."""

    allowed = {r.value for r in roles}

    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            user = current_user()
            if user is None:
                raise UnauthorizedError("Authentication required")
            if user.role.value not in allowed:
                raise ForbiddenError("Insufficient role for this action")
            return view(*args, **kwargs)

        return wrapper

    return decorator
