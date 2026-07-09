"""Project use cases (create, list)."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.project import Project
from backend.modules.laboratory.dto.project_dto import (
    CreateProjectRequest,
    project_to_dict,
)


class CreateProjectUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreateProjectRequest) -> dict:
        project = Project(project_code=request.project_code, name=request.name)
        with self._uow_factory() as uow:
            uow.projects.add(project)
        return project_to_dict(project)


class ListProjectsUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self) -> dict:
        with self._uow_factory() as uow:
            items = [project_to_dict(p) for p in uow.projects.list()]
        return {"count": len(items), "items": items}
