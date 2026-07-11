"""Staff repository.

Converts between the Staff ORM model and the domain object. Does not manage
transactions.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.project_orm import ProjectORM
from backend.infrastructure.orm.laboratory.staff_orm import StaffORM
from backend.modules.laboratory.domain.entities.staff import Staff


class StaffRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, staff: Staff) -> None:
        self.session.add(self._to_orm(staff))

    def get(self, staff_id: str) -> Staff | None:
        orm = self.session.get(StaffORM, staff_id)
        return self._to_domain(orm) if orm else None

    def list(self) -> list[Staff]:
        stmt = select(StaffORM).order_by(StaffORM.created_at)
        return [self._to_domain(o) for o in self.session.scalars(stmt).all()]

    def set_active(self, staff_id: str, active: bool) -> bool:
        orm = self.session.get(StaffORM, staff_id)
        if orm is None:
            return False
        orm.active = active
        return True

    def _to_orm(self, staff: Staff) -> StaffORM:
        projects = []
        if staff.qualified_project_ids:
            projects = list(
                self.session.scalars(
                    select(ProjectORM).where(ProjectORM.id.in_(staff.qualified_project_ids))
                ).all()
            )
        return StaffORM(
            id=staff.id,
            staff_code=staff.staff_code,
            name=staff.name,
            availability=[list(w) for w in staff.availability],
            projects=projects,
            active=staff.active,
        )

    @staticmethod
    def _to_domain(orm: StaffORM) -> Staff:
        return Staff(
            id=orm.id,
            staff_code=orm.staff_code,
            name=orm.name,
            availability=[tuple(w) for w in (orm.availability or [])],
            qualified_project_ids={p.id for p in orm.projects},
            active=orm.active,
        )
