"""Project use cases (create, list)."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.project import Project
from backend.modules.laboratory.dto.project_dto import (
    CreateProjectRequest,
    project_to_dict,
)
from backend.shared.errors import ConflictError, NotFoundError


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


class UpdateProjectUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, project_id: str, request: CreateProjectRequest) -> dict:
        with self._uow_factory() as uow:
            ok = uow.projects.update(
                project_id, project_code=request.project_code, name=request.name
            )
            if not ok:
                raise NotFoundError(f"Project {project_id} not found")
        return {"id": project_id, "projectCode": request.project_code, "name": request.name}


class DeleteProjectUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, project_id: str) -> dict:
        with self._uow_factory() as uow:
            if uow.workflow_definitions.count_for_project(project_id):
                raise ConflictError("Project has workflows; delete or reassign them first")
            if not uow.projects.delete(project_id):
                raise NotFoundError(f"Project {project_id} not found")
        return {"id": project_id, "deleted": True}
