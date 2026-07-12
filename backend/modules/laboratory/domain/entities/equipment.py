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
    # Global downtime days (maintenance / repair), "YYYY-MM-DD"; the machine can't
    # be scheduled on these days in any plan (ADR-021).
    unavailable_dates: list[str] = field(default_factory=list)
    # Overtime: weekend/holiday dates this machine is explicitly available on
    # (a non-working day turned into a working day for this resource, ADR-022).
    overtime_dates: list[str] = field(default_factory=list)
    # Projects this equipment is applicable to; used to scope which methods can
    # be bound to it (ADR-018).
    applicable_project_ids: set[str] = field(default_factory=set)
    # Methods (operation definitions) this equipment is bound to (ADR-015/018).
    method_ids: set[str] = field(default_factory=set)
    # FV validation (ADR-019): every machine must be validated periodically.
    # In hours now (ADR-025): fv_duration = hours an FV occupies; fv_validity =
    # hours an FV stays valid. Defaults: 8h (one shift) valid for 112h (14x8h).
    fv_duration: int = 8
    fv_validity: int = 112
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.equipment_code:
            raise ValidationError("equipmentCode is required")
        if not self.name:
            raise ValidationError("name is required")
