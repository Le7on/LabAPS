"""Staff entity.

A laboratory operator qualified for a set of Projects. Pure Python domain object
in the Laboratory Definition domain (separate from Planning, ADR-010).

A staff member's competency is expressed solely as the set of Projects it is
qualified for (ADR-017). The scheduler matches staff to a method by the Project
of the method's workflow: a staff member is eligible when that Project is among
its qualified projects. There is no separate free-text skill or expiring
qualification concept anymore.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class Staff:
    staff_code: str
    name: str
    # Projects this staff member is qualified for (ADR-017). This is the "Skill"
    # surfaced in the UI: which projects' work the staff may perform.
    qualified_project_ids: set[str] = field(default_factory=set)
    # Availability windows [start, end); empty means always available (Calendar).
    availability: list[tuple[int, int]] = field(default_factory=list)
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.staff_code:
            raise ValidationError("staffCode is required")
        if not self.name:
            raise ValidationError("name is required")
        for start, end in self.availability:
            if end <= start:
                raise ValidationError("availability window end must be after start")

    def is_qualified_for(self, project_id: str) -> bool:
        return project_id in self.qualified_project_ids

    def deactivate(self) -> None:
        self.active = False
