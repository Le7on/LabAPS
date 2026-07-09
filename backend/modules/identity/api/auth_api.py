"""Identity REST API — current user and user management (ADR-013).

Envelope responses (ADR-012). Creating users requires the administrator role;
`whoami` returns the authenticated user.
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.identity.application.manage_users import CreateUserUseCase
from backend.modules.identity.domain.role import Role
from backend.shared import api_response
from backend.shared.auth import current_user, require_role
from backend.shared.errors import ValidationError

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/auth/whoami")
def whoami():
    user = current_user()
    return api_response.success({"id": user.id, "username": user.username, "role": user.role.value})


@auth_bp.post("/users")
@require_role(Role.ADMINISTRATOR)
def create_user():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    use_case = CreateUserUseCase(current_app.config["CONTAINER"].auth_service)
    result = use_case.execute(data.get("username", ""), data.get("role", ""))
    return api_response.success(result, status=201)
