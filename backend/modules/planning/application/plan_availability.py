"""Per-plan resource availability use cases.

Lists the staff (qualified for any project) and equipment relevant to a plan with
their availability for that plan, and sets a resource available/unavailable for
the plan. Default (no explicit setting) is available.
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError, ValidationError

_KINDS = {"staff", "equipment"}


class GetPlanAvailabilityUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str) -> dict:
        with self._uow_factory() as uow:
            if uow.plans.get(plan_id) is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            settings = uow.plan_availability.settings(plan_id)

            def entry(kind, rid):
                s = settings[kind].get(rid, {})
                return s.get("available", True), s.get("unavailableDates", [])

            staff = []
            for s in uow.staff.list():
                avail, dates = entry("staff", s.id)
                staff.append(
                    {
                        "id": s.id,
                        "code": s.staff_code,
                        "name": s.name,
                        "qualifiedProjectIds": sorted(s.qualified_project_ids),
                        "available": avail,
                        "unavailableDates": dates,
                    }
                )
            equipment = []
            for e in uow.equipment.list():
                avail, dates = entry("equipment", e.id)
                equipment.append(
                    {
                        "id": e.id,
                        "code": e.equipment_code,
                        "name": e.name,
                        "methodIds": sorted(e.method_ids),
                        "available": avail,
                        "unavailableDates": dates,
                    }
                )

        return {"staff": staff, "equipment": equipment}


class SetPlanAvailabilityUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(
        self,
        plan_id: str,
        kind: str,
        resource_id: str,
        available: bool = True,
        unavailable_dates: list | None = None,
    ) -> dict:
        if kind not in _KINDS:
            raise ValidationError(f"Unknown resource kind: {kind}")
        ranges = [list(r) for r in (unavailable_dates or [])]
        for r in ranges:
            if len(r) != 2 or r[1] < r[0]:
                raise ValidationError(f"Invalid date range: {r}")
        with self._uow_factory() as uow:
            if uow.plans.get(plan_id) is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            uow.plan_availability.set(plan_id, kind, resource_id, available, ranges)

        return {
            "planId": plan_id,
            "kind": kind,
            "resourceId": resource_id,
            "available": available,
            "unavailableDates": ranges,
        }
