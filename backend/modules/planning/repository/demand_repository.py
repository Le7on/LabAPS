"""Demand repository.

Converts between the Demand ORM model and the domain entity for a Plan Version.
Does not manage transactions.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.planning.demand_orm import DemandORM
from backend.modules.planning.domain.entities.demand import Demand, DemandPriority


class DemandRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, plan_version_id: str, demand: Demand) -> None:
        self.session.add(
            DemandORM(
                id=demand.id,
                plan_version_id=plan_version_id,
                project_id=demand.project_id,
                quantity=demand.quantity,
                priority=demand.priority.value,
            )
        )

    def list_for_version(self, plan_version_id: str) -> list[Demand]:
        stmt = (
            select(DemandORM)
            .where(DemandORM.plan_version_id == plan_version_id)
            .order_by(DemandORM.created_at)
        )
        return [
            Demand(
                id=d.id,
                project_id=d.project_id,
                quantity=d.quantity,
                priority=DemandPriority(d.priority),
            )
            for d in self.session.scalars(stmt).all()
        ]
