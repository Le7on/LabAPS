"""Create Staff use case (one Unit of Work)."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.staff import Staff
from backend.modules.laboratory.dto.staff_dto import CreateStaffRequest, staff_to_dict


class CreateStaffUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreateStaffRequest) -> dict:
        staff = Staff(
            staff_code=request.staff_code,
            name=request.name,
            skills=request.skills,
        )

        with self._uow_factory() as uow:
            uow.staff.add(staff)

        return staff_to_dict(staff)
