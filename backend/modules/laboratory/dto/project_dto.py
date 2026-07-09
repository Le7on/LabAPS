"""Project DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from backend.modules.laboratory.domain.entities.project import Project


@dataclass(slots=True)
class CreateProjectRequest:
    project_code: str
    name: str

    @classmethod
    def from_json(cls, data: dict) -> CreateProjectRequest:
        return cls(
            project_code=data.get("projectCode", ""),
            name=data.get("name", ""),
        )


def project_to_dict(project: Project) -> dict:
    return {
        "id": project.id,
        "projectCode": project.project_code,
        "name": project.name,
        "active": project.active,
    }
