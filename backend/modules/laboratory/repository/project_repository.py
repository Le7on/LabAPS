"""Project repository (ORM <-> domain conversion; no transactions)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.project_orm import ProjectORM
from backend.modules.laboratory.domain.entities.project import Project


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, project: Project) -> None:
        self.session.add(self._to_orm(project))

    def get(self, project_id: str) -> Project | None:
        orm = self.session.get(ProjectORM, project_id)
        return self._to_domain(orm) if orm else None

    def list(self) -> list[Project]:
        stmt = select(ProjectORM).order_by(ProjectORM.created_at)
        return [self._to_domain(o) for o in self.session.scalars(stmt).all()]

    def set_active(self, project_id: str, active: bool) -> bool:
        orm = self.session.get(ProjectORM, project_id)
        if orm is None:
            return False
        orm.active = active
        return True

    @staticmethod
    def _to_orm(project: Project) -> ProjectORM:
        return ProjectORM(
            id=project.id,
            project_code=project.project_code,
            name=project.name,
            active=project.active,
        )

    @staticmethod
    def _to_domain(orm: ProjectORM) -> Project:
        return Project(
            id=orm.id,
            project_code=orm.project_code,
            name=orm.name,
            active=orm.active,
        )
