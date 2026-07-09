"""Project entity.

A laboratory project that production demand is raised against (Business Object
Model: Project -> Workflow Definition). Pure Python domain object in the
Laboratory Definition domain (ADR-010).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class Project:
    project_code: str
    name: str
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.project_code:
            raise ValidationError("projectCode is required")
        if not self.name:
            raise ValidationError("name is required")

    def deactivate(self) -> None:
        self.active = False
