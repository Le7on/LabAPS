"""Plan repository.

One repository per Aggregate Root (Plan). Converts between ORM models and Domain
Objects. Does not manage transactions; the Use Case owns the session lifecycle.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.planning.plan_orm import (
    PlanDemandLineORM,
    PlanORM,
    PlanVersionORM,
)
from backend.modules.planning.domain.aggregates.plan import Plan
from backend.modules.planning.domain.entities.plan_demand_line import PlanDemandLine
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

        # Sync demand lines (append-only from the aggregate; replace to be safe).
        existing_lines = {line.id for line in orm.demand_lines}
        for line in plan.demand_lines:
            if line.id not in existing_lines:
                orm.demand_lines.append(
                    PlanDemandLineORM(
                        id=line.id,
                        workflow_definition_id=line.workflow_definition_id,
                        operation_definition_id=line.operation_definition_id,
                        rounds=line.rounds,
                        target_date=line.target_date,
                    )
                )

        existing = {v.id: v for v in orm.versions}
        for version in plan.versions:
            if version.id in existing:
                # Sync mutable state on existing versions (e.g. lifecycle status).
                orm_version = existing[version.id]
                orm_version.version_type = version.version_type.value
                orm_version.status = version.status.value
            else:
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

    def remove_demand_line(self, plan_id: str, line_id: str) -> bool:
        orm = self.session.get(PlanORM, plan_id)
        if orm is None:
            return False
        line = next((line_ for line_ in orm.demand_lines if line_.id == line_id), None)
        if line is None:
            return False
        orm.demand_lines.remove(line)
        return True

    def delete(self, plan_id: str) -> bool:
        orm = self.session.get(PlanORM, plan_id)
        if orm is None:
            return False
        self.session.delete(orm)
        return True

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
            start_date=plan.start_date,
            end_date=plan.end_date,
            shift_mode=plan.shift_mode,
            skipped_dates=list(plan.skipped_dates),
            demand_lines=[
                PlanDemandLineORM(
                    id=line.id,
                    workflow_definition_id=line.workflow_definition_id,
                    operation_definition_id=line.operation_definition_id,
                    rounds=line.rounds,
                    target_date=line.target_date,
                )
                for line in plan.demand_lines
            ],
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
            start_date=orm.start_date,
            end_date=orm.end_date,
            shift_mode=orm.shift_mode or "single",
            skipped_dates=list(orm.skipped_dates or []),
            demand_lines=[
                PlanDemandLine(
                    id=line.id,
                    workflow_definition_id=line.workflow_definition_id,
                    operation_definition_id=line.operation_definition_id or "",
                    rounds=line.rounds,
                    target_date=line.target_date,
                )
                for line in orm.demand_lines
            ],
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
