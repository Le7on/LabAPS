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
    gelatin_type: str | None = None
    equipment_ids: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()

    @classmethod
    def from_json(cls, data: dict) -> OperationDefinitionInput:
        return cls(
            operation_type=data.get("operationType", ""),
            duration=int(data.get("duration", 0)),
            gelatin_type=data.get("gelatinType"),
            equipment_ids=tuple(data.get("equipmentIds", ())),
            depends_on=tuple(data.get("dependsOn", ())),
        )


@dataclass(slots=True)
class CreateWorkflowDefinitionRequest:
    workflow_code: str
    name: str
    project_id: str = ""
    operations: list[OperationDefinitionInput] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> CreateWorkflowDefinitionRequest:
        return cls(
            workflow_code=data.get("workflowCode", ""),
            name=data.get("name", ""),
            project_id=data.get("projectId", ""),
            operations=[
                OperationDefinitionInput.from_json(op) for op in data.get("operations", [])
            ],
        )


def workflow_definition_to_dict(workflow: WorkflowDefinition) -> dict:
    return {
        "id": workflow.id,
        "workflowCode": workflow.workflow_code,
        "name": workflow.name,
        "projectId": workflow.project_id,
        "active": workflow.active,
        "operations": [
            {
                "id": op.id,
                "operationType": op.operation_type,
                "duration": op.duration,
                "gelatinType": op.gelatin_type,
                "equipmentIds": list(op.equipment_ids),
                "dependsOn": list(op.depends_on),
            }
            for op in workflow.operations
        ],
    }
