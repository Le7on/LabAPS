"""Laboratory REST API — Equipment.

Adapts HTTP requests to Equipment use cases. No business logic.
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from backend.modules.laboratory.application.create_equipment import (
    CreateEquipmentUseCase,
)
from backend.modules.laboratory.application.list_equipment import ListEquipmentUseCase
from backend.modules.laboratory.dto.equipment_dto import CreateEquipmentRequest
from backend.shared.errors import ValidationError

equipment_bp = Blueprint("equipment", __name__)


def _session_factory():
    return current_app.config["CONTAINER"].session_factory


@equipment_bp.post("/equipment")
def create_equipment():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    use_case = CreateEquipmentUseCase(_session_factory())
    return jsonify(use_case.execute(CreateEquipmentRequest.from_json(data))), 201


@equipment_bp.get("/equipment")
def list_equipment():
    use_case = ListEquipmentUseCase(_session_factory())
    return jsonify(use_case.execute()), 200
