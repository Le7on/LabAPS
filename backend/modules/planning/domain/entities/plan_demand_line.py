"""Plan Demand Line entity.

One line of a PI's plan request: run a given Workflow a number of rounds on a
specific target date (a hard-constraint date). Belongs to the Plan aggregate.
Pure Python; no framework dependencies.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class PlanDemandLine:
    workflow_definition_id: str
    rounds: int
    target_date: str  # "YYYY-MM-DD"; the day these rounds must run (hard constraint)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.workflow_definition_id:
            raise ValidationError("workflowDefinitionId is required")
        if self.rounds <= 0:
            raise ValidationError("rounds must be positive")
        if not self.target_date:
            raise ValidationError("targetDate is required")
