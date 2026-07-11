"""Laboratory REST API — Staff.

Adapts HTTP requests to Staff use cases. No business logic. Envelope responses
(ADR-012).
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.laboratory.application.create_staff import (
    CreateStaffUseCase,
    DeleteStaffUseCase,
    UpdateStaffUseCase,
)
from backend.modules.laboratory.application.list_staff import ListStaffUseCase
from backend.modules.laboratory.application.set_resource_active import (
    SetResourceActiveUseCase,
)
from backend.modules.laboratory.dto.staff_dto import CreateStaffRequest
from backend.shared import api_response
from backend.shared.errors import ValidationError

staff_bp = Blueprint("staff", __name__)


def _uow():
    return current_app.config["CONTAINER"].unit_of_work


@staff_bp.post("/staff")
def create_staff():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    use_case = CreateStaffUseCase(_uow())
    result = use_case.execute(CreateStaffRequest.from_json(data))
    return api_response.success(result, status=201)


@staff_bp.get("/staff")
def list_staff():
    use_case = ListStaffUseCase(_uow())
    result = use_case.execute()
    return api_response.collection(result["items"])


@staff_bp.put("/staff/<staff_id>")
def update_staff(staff_id: str):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    use_case = UpdateStaffUseCase(_uow())
    return api_response.success(use_case.execute(staff_id, CreateStaffRequest.from_json(data)))


@staff_bp.delete("/staff/<staff_id>")
def delete_staff(staff_id: str):
    use_case = DeleteStaffUseCase(_uow())
    return api_response.success(use_case.execute(staff_id))


@staff_bp.post("/staff/<staff_id>/deactivate")
def deactivate_staff(staff_id: str):
    use_case = SetResourceActiveUseCase(_uow())
    return api_response.success(use_case.execute("staff", staff_id, False))


@staff_bp.post("/staff/<staff_id>/activate")
def activate_staff(staff_id: str):
    use_case = SetResourceActiveUseCase(_uow())
    return api_response.success(use_case.execute("staff", staff_id, True))
