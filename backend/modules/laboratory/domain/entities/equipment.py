"""Equipment entity.

Laboratory resource in the Laboratory Definition domain (ADR-010). Equipment is
declared applicable to a set of Projects, and bound to specific Methods of those
projects' workflows (ADR-018). The scheduler restricts a method to the equipment
bound to it.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class Equipment:
    equipment_code: str
    name: str
    # Availability windows [start, end); empty means always available (Calendar).
    availability: list[tuple[int, int]] = field(default_factory=list)
    # Projects this equipment is applicable to; used to scope which methods can
    # be bound to it (ADR-018).
    applicable_project_ids: set[str] = field(default_factory=set)
    # Methods (operation definitions) this equipment is bound to (ADR-015/018).
    method_ids: set[str] = field(default_factory=set)
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.equipment_code:
            raise ValidationError("equipmentCode is required")
        if not self.name:
            raise ValidationError("name is required")
        for start, end in self.availability:
            if end <= start:
                raise ValidationError("availability window end must be after start")
