"""Set a resource's global unavailable dates (ADR-021).

Staff leave / equipment maintenance days that apply across all plans. Dates are
"YYYY-MM-DD"; the scheduler excludes these days for the resource.
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError, ValidationError

_KINDS = {"equipment", "staff"}


class SetResourceAvailabilityUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, resource_kind: str, resource_id: str, unavailable_dates: list) -> dict:
        if resource_kind not in _KINDS:
            raise ValidationError(f"Unknown resource kind: {resource_kind}")
        dates = sorted({str(d) for d in (unavailable_dates or [])})

        with self._uow_factory() as uow:
            repo = getattr(uow, resource_kind)
            if not repo.set_unavailable_dates(resource_id, dates):
                raise NotFoundError(f"{resource_kind} {resource_id} not found")

        return {"id": resource_id, "unavailableDates": dates}
