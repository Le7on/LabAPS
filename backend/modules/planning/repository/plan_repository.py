"""Plan repository.

One repository per Aggregate Root (Plan). Converts between ORM models and Domain
Objects. Does not manage transactions; the Use Case owns the session lifecycle.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.planning.plan_orm import PlanORM, PlanVersionORM
from backend.modules.planning.domain.aggregates.plan import Plan
from backend.modules.planning.domain.entities.plan_version import PlanVersion
from backend.modules.planning.domain.enums.plan_enums import (
    PlanStatus,
    PlanVersionStatus,
    VersionType,
)


class PlanRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, plan: Plan) -> None:
        self.session.add(self._to_orm(plan))

    def save(self, plan: Plan) -> None:
        """Persist changes to an existing aggregate (e.g. a new version).

        Loads the aggregate root and syncs its owned children, honoring the rule
        that child entities are never updated directly.
        """

        orm = self.session.get(PlanORM, plan.id)
        if orm is None:
            self.session.add(self._to_orm(plan))
            return

        orm.name = plan.name
        orm.description = plan.description
        orm.status = plan.status.value

        existing_ids = {v.id for v in orm.versions}
        for version in plan.versions:
            if version.id not in existing_ids:
                orm.versions.append(
                    PlanVersionORM(
                        id=version.id,
                        version_number=version.version_number,
                        version_type=version.version_type.value,
                        status=version.status.value,
                    )
                )

    def get(self, plan_id: str) -> Plan | None:
        orm = self.session.get(PlanORM, plan_id)
        return self._to_domain(orm) if orm else None

    def list(self) -> list[Plan]:
        stmt = select(PlanORM).order_by(PlanORM.created_at)
        return [self._to_domain(orm) for orm in self.session.scalars(stmt).all()]

    def count(self) -> int:
        return len(self.session.scalars(select(PlanORM.id)).all())

    # -- mapping ---------------------------------------------------------

    @staticmethod
    def _to_orm(plan: Plan) -> PlanORM:
        return PlanORM(
            id=plan.id,
            plan_code=plan.plan_code,
            name=plan.name,
            description=plan.description,
            planning_horizon=plan.planning_horizon,
            status=plan.status.value,
            versions=[
                PlanVersionORM(
                    id=v.id,
                    version_number=v.version_number,
                    version_type=v.version_type.value,
                    status=v.status.value,
                )
                for v in plan.versions
            ],
        )

    @staticmethod
    def _to_domain(orm: PlanORM) -> Plan:
        return Plan(
            id=orm.id,
            plan_code=orm.plan_code,
            name=orm.name,
            description=orm.description,
            planning_horizon=orm.planning_horizon,
            status=PlanStatus(orm.status),
            created_at=orm.created_at,
            versions=[
                PlanVersion(
                    id=v.id,
                    version_number=v.version_number,
                    version_type=VersionType(v.version_type),
                    status=PlanVersionStatus(v.status),
                    created_at=v.created_at,
                )
                for v in orm.versions
            ],
        )
