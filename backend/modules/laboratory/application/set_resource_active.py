"""Activate / deactivate a laboratory resource (equipment, staff, project).

Deactivation is a reversible state change; deactivated resources are excluded
from scheduling (the Planning Context snapshot only captures active resources).
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError, ValidationError

_REPOS = {"equipment", "staff", "projects"}


class SetResourceActiveUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, resource_kind: str, resource_id: str, active: bool) -> dict:
        if resource_kind not in _REPOS:
            raise ValidationError(f"Unknown resource kind: {resource_kind}")

        with self._uow_factory() as uow:
            repo = getattr(uow, resource_kind)
            if not repo.set_active(resource_id, active):
                raise NotFoundError(f"{resource_kind} {resource_id} not found")

        return {"id": resource_id, "active": active}
