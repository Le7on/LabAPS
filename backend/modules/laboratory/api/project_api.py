"""Laboratory REST API — Projects.

Adapts HTTP requests to Project use cases. No business logic. Envelope responses
(ADR-012).
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.laboratory.application.manage_projects import (
    CreateProjectUseCase,
    ListProjectsUseCase,
)
from backend.modules.laboratory.application.set_resource_active import (
    SetResourceActiveUseCase,
)
from backend.modules.laboratory.dto.project_dto import CreateProjectRequest
from backend.shared import api_response
from backend.shared.errors import ValidationError

project_bp = Blueprint("project", __name__)


def _uow():
    return current_app.config["CONTAINER"].unit_of_work


@project_bp.post("/projects")
def create_project():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    use_case = CreateProjectUseCase(_uow())
    return api_response.success(use_case.execute(CreateProjectRequest.from_json(data)), status=201)


@project_bp.get("/projects")
def list_projects():
    use_case = ListProjectsUseCase(_uow())
    return api_response.collection(use_case.execute()["items"])


@project_bp.post("/projects/<project_id>/deactivate")
def deactivate_project(project_id: str):
    use_case = SetResourceActiveUseCase(_uow())
    return api_response.success(use_case.execute("projects", project_id, False))


@project_bp.post("/projects/<project_id>/activate")
def activate_project(project_id: str):
    use_case = SetResourceActiveUseCase(_uow())
    return api_response.success(use_case.execute("projects", project_id, True))
