"""List Plans use case (read operation)."""

from __future__ import annotations

from backend.modules.planning.dto.plan_dto import plan_to_dict


class ListPlansUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self) -> dict:
        with self._uow_factory() as uow:
            items = [plan_to_dict(p) for p in uow.plans.list()]

        return {"count": len(items), "items": items}
