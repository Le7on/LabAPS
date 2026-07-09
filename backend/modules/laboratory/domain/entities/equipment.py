"""Equipment entity.

Laboratory resource with a capability set. Pure Python domain object; belongs to
the Laboratory Definition domain, which is separate from Planning (ADR-010).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class Equipment:
    equipment_code: str
    name: str
    capabilities: set[str] = field(default_factory=set)
    # Availability windows [start, end); empty means always available (Calendar).
    availability: list[tuple[int, int]] = field(default_factory=list)
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

    def has_capability(self, capability: str) -> bool:
        return capability in self.capabilities
