"""Laboratory REST API — Equipment.

Adapts HTTP requests to Equipment use cases. No business logic.
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.laboratory.application.create_equipment import (
    CreateEquipmentUseCase,
)
from backend.modules.laboratory.application.list_equipment import ListEquipmentUseCase
from backend.modules.laboratory.dto.equipment_dto import CreateEquipmentRequest
from backend.shared import api_response
from backend.shared.errors import ValidationError

equipment_bp = Blueprint("equipment", __name__)


def _uow():
    return current_app.config["CONTAINER"].unit_of_work


@equipment_bp.post("/equipment")
def create_equipment():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    use_case = CreateEquipmentUseCase(_uow())
    result = use_case.execute(CreateEquipmentRequest.from_json(data))
    return api_response.success(result, status=201)


@equipment_bp.get("/equipment")
def list_equipment():
    use_case = ListEquipmentUseCase(_uow())
    result = use_case.execute()
    return api_response.collection(result["items"])
