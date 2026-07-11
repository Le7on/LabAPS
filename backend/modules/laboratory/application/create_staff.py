"""Create Staff use case (one Unit of Work)."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.staff import Staff
from backend.modules.laboratory.dto.staff_dto import CreateStaffRequest, staff_to_dict
from backend.shared.errors import NotFoundError, ValidationError


def _validate_projects(uow, request):
    for project_id in request.qualified_project_ids:
        if uow.projects.get(project_id) is None:
            raise ValidationError(f"Unknown project: {project_id}")


class CreateStaffUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreateStaffRequest) -> dict:
        staff = Staff(
            staff_code=request.staff_code,
            name=request.name,
            availability=request.availability,
            qualified_project_ids=request.qualified_project_ids,
        )

        with self._uow_factory() as uow:
            _validate_projects(uow, request)
            uow.staff.add(staff)

        return staff_to_dict(staff)


class UpdateStaffUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, staff_id: str, request: CreateStaffRequest) -> dict:
        staff = Staff(
            id=staff_id,
            staff_code=request.staff_code,
            name=request.name,
            availability=request.availability,
            qualified_project_ids=request.qualified_project_ids,
        )
        with self._uow_factory() as uow:
            _validate_projects(uow, request)
            if not uow.staff.update(staff):
                raise NotFoundError(f"Staff {staff_id} not found")
        return staff_to_dict(staff)


class DeleteStaffUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, staff_id: str) -> dict:
        with self._uow_factory() as uow:
            if not uow.staff.delete(staff_id):
                raise NotFoundError(f"Staff {staff_id} not found")
        return {"id": staff_id, "deleted": True}
