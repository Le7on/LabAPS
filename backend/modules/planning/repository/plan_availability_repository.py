"""Per-plan resource availability repository.

Stores explicit availability settings for a plan; absence means available.
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

    def set(self, plan_id: str, kind: str, resource_id: str, available: bool) -> None:
        stmt = select(PlanResourceAvailabilityORM).where(
            PlanResourceAvailabilityORM.plan_id == plan_id,
            PlanResourceAvailabilityORM.resource_kind == kind,
            PlanResourceAvailabilityORM.resource_id == resource_id,
        )
        row = self.session.scalar(stmt)
        if row is None:
            self.session.add(
                PlanResourceAvailabilityORM(
                    plan_id=plan_id,
                    resource_kind=kind,
                    resource_id=resource_id,
                    available=available,
                )
            )
        else:
            row.available = available

    def unavailable_ids(self, plan_id: str, kind: str) -> set[str]:
        """Resource ids explicitly marked unavailable for this plan and kind."""
        stmt = select(PlanResourceAvailabilityORM.resource_id).where(
            PlanResourceAvailabilityORM.plan_id == plan_id,
            PlanResourceAvailabilityORM.resource_kind == kind,
            PlanResourceAvailabilityORM.available.is_(False),
        )
        return set(self.session.scalars(stmt).all())

    def settings(self, plan_id: str) -> dict[str, dict[str, bool]]:
        """All explicit settings for a plan: {kind: {resource_id: available}}."""
        stmt = select(PlanResourceAvailabilityORM).where(
            PlanResourceAvailabilityORM.plan_id == plan_id
        )
        out: dict[str, dict[str, bool]] = {"staff": {}, "equipment": {}}
        for row in self.session.scalars(stmt).all():
            out.setdefault(row.resource_kind, {})[row.resource_id] = row.available
        return out
