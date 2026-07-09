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
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operations: list[OperationDefinition] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.workflow_code:
            raise ValidationError("workflowCode is required")
        if not self.name:
            raise ValidationError("name is required")

    def add_operation(
        self,
        operation_type: str,
        duration: int,
        required_capability: str | None = None,
        required_skill: str | None = None,
        required_qualification: str | None = None,
        depends_on: tuple[str, ...] = (),
    ) -> OperationDefinition:
        """Add an operation definition to this workflow (aggregate-owned)."""

        operation = OperationDefinition(
            operation_type=operation_type,
            duration=duration,
            required_capability=required_capability,
            required_skill=required_skill,
            required_qualification=required_qualification,
            depends_on=depends_on,
        )
        self.operations.append(operation)
        return operation
