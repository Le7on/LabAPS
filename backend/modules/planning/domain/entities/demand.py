"""Demand entity.

A requested production quantity within a Plan Version (Table Dictionary: demand).
Belongs to the Plan Version aggregate. Pure Python; no framework dependencies.
Priority weights demand when the scheduler optimizes for completion.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import StrEnum

from backend.shared.errors import ValidationError


class DemandPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

    @property
    def weight(self) -> int:
        return {"low": 1, "normal": 2, "high": 4}[self.value]


@dataclass(slots=True)
class Demand:
    project_id: str
    quantity: int
    priority: DemandPriority = DemandPriority.NORMAL
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.project_id:
            raise ValidationError("projectId is required")
        if self.quantity <= 0:
            raise ValidationError("quantity must be positive")
