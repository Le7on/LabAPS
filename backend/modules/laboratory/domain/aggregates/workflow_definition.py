"""Workflow Definition aggregate root.

A reusable workflow template in the Laboratory Definition domain (ADR-003:
Workflow Definition vs Workflow Instance). It owns its Operation Definitions;
only the aggregate root adds or modifies them (Domain Entity Template, aggregate
consistency). Pure Python, no framework dependencies.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.modules.laboratory.domain.entities.operation_definition import (
    OperationDefinition,
)
from backend.shared.errors import ValidationError


@dataclass(slots=True)
class WorkflowDefinition:
    workflow_code: str
    name: str
    # A workflow is defined for exactly one project (ADR-015, SSOT section 6).
    project_id: str = ""
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operations: list[OperationDefinition] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.workflow_code:
            raise ValidationError("workflowCode is required")
        if not self.name:
            raise ValidationError("name is required")
        if not self.project_id:
            raise ValidationError("projectId is required")

    def add_operation(
        self,
        operation_type: str,
        duration: int,
        gelatin_type: str | None = None,
        equipment_ids: tuple[str, ...] = (),
        depends_on: tuple[str, ...] = (),
    ) -> OperationDefinition:
        """Add a method (operation definition) to this workflow (aggregate-owned)."""

        operation = OperationDefinition(
            operation_type=operation_type,
            duration=duration,
            gelatin_type=gelatin_type,
            equipment_ids=equipment_ids,
            depends_on=depends_on,
        )
        self.operations.append(operation)
        return operation
