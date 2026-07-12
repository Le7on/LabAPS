"""Set a resource's global availability dates (ADR-021 / ADR-022).

- unavailable_dates: staff leave / equipment maintenance days (excluded).
- overtime_dates: weekend/holiday days the resource is explicitly available on
  (a non-working day turned into a working day for this resource).

Dates are "YYYY-MM-DD" and apply across all plans.
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError, ValidationError

_KINDS = {"equipment", "staff"}


class SetResourceAvailabilityUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(
        self,
        resource_kind: str,
        resource_id: str,
        unavailable_dates: list,
        overtime_dates: list | None = None,
    ) -> dict:
        if resource_kind not in _KINDS:
            raise ValidationError(f"Unknown resource kind: {resource_kind}")
        unavailable = sorted({str(d) for d in (unavailable_dates or [])})
        overtime = sorted({str(d) for d in (overtime_dates or [])})

        with self._uow_factory() as uow:
            repo = getattr(uow, resource_kind)
            if not repo.set_availability(resource_id, unavailable, overtime):
                raise NotFoundError(f"{resource_kind} {resource_id} not found")

        return {
            "id": resource_id,
            "unavailableDates": unavailable,
            "overtimeDates": overtime,
        }
