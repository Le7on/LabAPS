"""Operation Definition entity.

A step template within a Workflow Definition. Belongs to the Workflow Definition
aggregate. Carries the scheduling requirements of an operation (Business Object
Model section 8): operation type, duration, required capability, required skill
and dependencies. It never stores concrete resources — those belong to
Assignment.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class OperationDefinition:
    operation_type: str
    duration: int
    required_capability: str | None = None
    required_skill: str | None = None
    depends_on: tuple[str, ...] = ()
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.operation_type:
            raise ValidationError("operationType is required")
        if self.duration <= 0:
            raise ValidationError("duration must be positive")
