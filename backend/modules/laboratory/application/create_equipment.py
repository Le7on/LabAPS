"""Create Equipment use case (one Unit of Work)."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.equipment import Equipment
from backend.modules.laboratory.dto.equipment_dto import (
    CreateEquipmentRequest,
    equipment_to_dict,
)
from backend.shared.errors import NotFoundError, ValidationError


def _validate_refs(uow, request):
    for project_id in request.applicable_project_ids:
        if uow.projects.get(project_id) is None:
            raise ValidationError(f"Unknown project: {project_id}")
    for method_id in request.method_ids:
        if uow.workflow_definitions.get_operation(method_id) is None:
            raise ValidationError(f"Unknown method: {method_id}")


class CreateEquipmentUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreateEquipmentRequest) -> dict:
        equipment = Equipment(
            equipment_code=request.equipment_code,
            name=request.name,
            availability=request.availability,
            applicable_project_ids=request.applicable_project_ids,
            method_ids=request.method_ids,
        )

        with self._uow_factory() as uow:
            _validate_refs(uow, request)
            uow.equipment.add(equipment)

        return equipment_to_dict(equipment)


class UpdateEquipmentUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, equipment_id: str, request: CreateEquipmentRequest) -> dict:
        equipment = Equipment(
            id=equipment_id,
            equipment_code=request.equipment_code,
            name=request.name,
            availability=request.availability,
            applicable_project_ids=request.applicable_project_ids,
            method_ids=request.method_ids,
        )
        with self._uow_factory() as uow:
            _validate_refs(uow, request)
            if not uow.equipment.update(equipment):
                raise NotFoundError(f"Equipment {equipment_id} not found")
        return equipment_to_dict(equipment)


class DeleteEquipmentUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, equipment_id: str) -> dict:
        with self._uow_factory() as uow:
            if not uow.equipment.delete(equipment_id):
                raise NotFoundError(f"Equipment {equipment_id} not found")
        return {"id": equipment_id, "deleted": True}
