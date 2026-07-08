"""Laboratory REST API — Staff.

Adapts HTTP requests to Staff use cases. No business logic. Envelope responses
(ADR-012).
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.laboratory.application.create_staff import CreateStaffUseCase
from backend.modules.laboratory.application.list_staff import ListStaffUseCase
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
