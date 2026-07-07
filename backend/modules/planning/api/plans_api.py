"""Planning REST API — Plans.

Adapts HTTP requests to Plan use cases. Request parsing, DTO conversion and HTTP
responses only; no business logic (Development Guide, project structure section 9).
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.planning.application.create_plan import CreatePlanUseCase
from backend.modules.planning.application.create_plan_version import (
    CreatePlanVersionUseCase,
)
from backend.modules.planning.application.generate_schedule import (
    GenerateScheduleUseCase,
)
from backend.modules.planning.application.get_plan import GetPlanUseCase
from backend.modules.planning.application.list_plans import ListPlansUseCase
from backend.modules.planning.dto.plan_dto import CreatePlanRequest
from backend.shared import api_response
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
    return api_response.success(result, status=201)


@plans_bp.get("/plans")
def list_plans():
    use_case = ListPlansUseCase(_container().session_factory)
    result = use_case.execute()
    return api_response.collection(result["items"])


@plans_bp.get("/plans/<plan_id>")
def get_plan(plan_id: str):
    use_case = GetPlanUseCase(_container().session_factory)
    return api_response.success(use_case.execute(plan_id))


@plans_bp.post("/plans/<plan_id>/versions")
def create_plan_version(plan_id: str):
    use_case = CreatePlanVersionUseCase(_container().session_factory)
    return api_response.success(use_case.execute(plan_id), status=201)


@plans_bp.post("/plans/<plan_id>/versions/<version_id>/schedule")
def generate_schedule(plan_id: str, version_id: str):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    container = _container()
    use_case = GenerateScheduleUseCase(container.session_factory, container.scheduling_engine)
    operations = data.get("operations", [])
    result = use_case.execute(plan_id, version_id, operations)

    # Command response: updated resource in data, execution info in meta (ADR-012).
    meta = {
        "makespan": result.pop("makespan"),
        "feasible": result.pop("feasible"),
        "runtimeStatus": result["status"],
    }
    return api_response.success(result, meta=meta)
