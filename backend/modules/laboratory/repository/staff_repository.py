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

    def update(self, staff: Staff) -> bool:
        orm = self.session.get(StaffORM, staff.id)
        if orm is None:
            return False
        orm.staff_code = staff.staff_code
        orm.name = staff.name
        orm.unavailable_dates = list(staff.unavailable_dates)
        orm.projects = self._resolve_projects(staff.qualified_project_ids)
        return True

    def delete(self, staff_id: str) -> bool:
        orm = self.session.get(StaffORM, staff_id)
        if orm is None:
            return False
        self.session.delete(orm)
        return True

    def set_unavailable_dates(self, staff_id: str, dates: list) -> bool:
        orm = self.session.get(StaffORM, staff_id)
        if orm is None:
            return False
        orm.unavailable_dates = list(dates)
        return True

    def _resolve_projects(self, ids):
        if not ids:
            return []
        return list(self.session.scalars(select(ProjectORM).where(ProjectORM.id.in_(ids))).all())

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
            unavailable_dates=list(staff.unavailable_dates),
            projects=projects,
            active=staff.active,
        )

    @staticmethod
    def _to_domain(orm: StaffORM) -> Staff:
        return Staff(
            id=orm.id,
            staff_code=orm.staff_code,
            name=orm.name,
            unavailable_dates=list(orm.unavailable_dates or []),
            qualified_project_ids={p.id for p in orm.projects},
            active=orm.active,
        )
