"""User management use cases (ADR-013)."""

from __future__ import annotations

from backend.modules.identity.application.auth_service import AuthService
from backend.modules.identity.domain.role import Role
from backend.shared.errors import ValidationError


class CreateUserUseCase:
    def __init__(self, auth_service: AuthService):
        self._auth = auth_service

    def execute(self, username: str, role: str) -> dict:
        if not username:
            raise ValidationError("username is required")
        try:
            role_value = Role(role)
        except ValueError as exc:
            raise ValidationError(f"Unknown role: {role}") from exc

        return self._auth.create_user(username, role_value)
