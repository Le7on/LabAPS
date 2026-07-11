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
    duration: int  # number of shifts occupied (1 shift = 1 scheduler time unit)
    gelatin_type: str | None = None
    # Equipment bound to this method (ADR-015): the scheduler's equipment
    # candidates for the method are exactly these. Staff eligibility comes from
    # the workflow's project (ADR-017), not from per-method skill strings.
    equipment_ids: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.operation_type:
            raise ValidationError("operationType is required")
        if self.duration <= 0:
            raise ValidationError("duration must be positive")
