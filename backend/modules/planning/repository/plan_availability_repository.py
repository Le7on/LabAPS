"""Per-plan resource availability repository.

Stores explicit availability for a plan; absence means fully available. A row can
mark a resource off for the whole plan (available=False) and/or list unavailable
date ranges (leave, breakdown), each ["YYYY-MM-DD", "YYYY-MM-DD"] inclusive.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.planning.plan_resource_availability_orm import (
    PlanResourceAvailabilityORM,
)


class PlanAvailabilityRepository:
    def __init__(self, session: Session):
        self.session = session

    def _row(self, plan_id, kind, resource_id):
        stmt = select(PlanResourceAvailabilityORM).where(
            PlanResourceAvailabilityORM.plan_id == plan_id,
            PlanResourceAvailabilityORM.resource_kind == kind,
            PlanResourceAvailabilityORM.resource_id == resource_id,
        )
        return self.session.scalar(stmt)

    def set(
        self,
        plan_id: str,
        kind: str,
        resource_id: str,
        available: bool = True,
        unavailable_dates: list | None = None,
    ) -> None:
        dates = [list(r) for r in (unavailable_dates or [])]
        row = self._row(plan_id, kind, resource_id)
        if row is None:
            self.session.add(
                PlanResourceAvailabilityORM(
                    plan_id=plan_id,
                    resource_kind=kind,
                    resource_id=resource_id,
                    available=available,
                    unavailable_dates=dates,
                )
            )
        else:
            row.available = available
            row.unavailable_dates = dates

    def unavailable_ids(self, plan_id: str, kind: str) -> set[str]:
        """Resource ids marked off for the whole plan (available=False)."""
        stmt = select(PlanResourceAvailabilityORM.resource_id).where(
            PlanResourceAvailabilityORM.plan_id == plan_id,
            PlanResourceAvailabilityORM.resource_kind == kind,
            PlanResourceAvailabilityORM.available.is_(False),
        )
        return set(self.session.scalars(stmt).all())

    def unavailable_dates(self, plan_id: str, kind: str) -> dict[str, list]:
        """Map resource_id -> list of unavailable [start, end] date ranges."""
        stmt = select(PlanResourceAvailabilityORM).where(
            PlanResourceAvailabilityORM.plan_id == plan_id,
            PlanResourceAvailabilityORM.resource_kind == kind,
        )
        out: dict[str, list] = {}
        for row in self.session.scalars(stmt).all():
            if row.unavailable_dates:
                out[row.resource_id] = [list(r) for r in row.unavailable_dates]
        return out

    def settings(self, plan_id: str) -> dict[str, dict[str, dict]]:
        """All explicit settings: {kind: {resource_id: {available, dates}}}."""
        stmt = select(PlanResourceAvailabilityORM).where(
            PlanResourceAvailabilityORM.plan_id == plan_id
        )
        out: dict[str, dict[str, dict]] = {"staff": {}, "equipment": {}}
        for row in self.session.scalars(stmt).all():
            out.setdefault(row.resource_kind, {})[row.resource_id] = {
                "available": row.available,
                "unavailableDates": [list(r) for r in (row.unavailable_dates or [])],
            }
        return out
