"""Planning REST API — Plans.

Adapts HTTP requests to Plan use cases. Request parsing, DTO conversion and HTTP
responses only; no business logic (Development Guide, project structure section 9).
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from backend.modules.planning.application.create_plan import CreatePlanUseCase
from backend.modules.planning.application.get_plan import GetPlanUseCase
from backend.modules.planning.application.list_plans import ListPlansUseCase
from backend.modules.planning.dto.plan_dto import CreatePlanRequest
from backend.shared.errors import ValidationError

plans_bp = Blueprint("plans", __name__)


def _container():
    return current_app.config["CONTAINER"]


@plans_bp.post("/plans")
def create_plan():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    use_case = CreatePlanUseCase(_container().session_factory)
    result = use_case.execute(CreatePlanRequest.from_json(data))
    return jsonify(result), 201


@plans_bp.get("/plans")
def list_plans():
    use_case = ListPlansUseCase(_container().session_factory)
    return jsonify(use_case.execute()), 200


@plans_bp.get("/plans/<plan_id>")
def get_plan(plan_id: str):
    use_case = GetPlanUseCase(_container().session_factory)
    return jsonify(use_case.execute(plan_id)), 200
