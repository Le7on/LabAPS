"""Workflow Definition DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.laboratory.domain.aggregates.workflow_definition import (
    WorkflowDefinition,
)


@dataclass(slots=True)
class OperationDefinitionInput:
    operation_type: str
    duration: int
    required_capability: str | None = None
    required_skill: str | None = None
    required_qualification: str | None = None
    depends_on: tuple[str, ...] = ()

    @classmethod
    def from_json(cls, data: dict) -> OperationDefinitionInput:
        return cls(
            operation_type=data.get("operationType", ""),
            duration=int(data.get("duration", 0)),
            required_capability=data.get("requiredCapability"),
            required_skill=data.get("requiredSkill"),
            required_qualification=data.get("requiredQualification"),
            depends_on=tuple(data.get("dependsOn", ())),
        )


@dataclass(slots=True)
class CreateWorkflowDefinitionRequest:
    workflow_code: str
    name: str
    operations: list[OperationDefinitionInput] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> CreateWorkflowDefinitionRequest:
        return cls(
            workflow_code=data.get("workflowCode", ""),
            name=data.get("name", ""),
            operations=[
                OperationDefinitionInput.from_json(op) for op in data.get("operations", [])
            ],
        )


def workflow_definition_to_dict(workflow: WorkflowDefinition) -> dict:
    return {
        "id": workflow.id,
        "workflowCode": workflow.workflow_code,
        "name": workflow.name,
        "active": workflow.active,
        "operations": [
            {
                "id": op.id,
                "operationType": op.operation_type,
                "duration": op.duration,
                "requiredCapability": op.required_capability,
                "requiredSkill": op.required_skill,
                "requiredQualification": op.required_qualification,
                "dependsOn": list(op.depends_on),
            }
            for op in workflow.operations
        ],
    }
