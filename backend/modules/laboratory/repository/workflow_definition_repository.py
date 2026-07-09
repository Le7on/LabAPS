"""Workflow Definition repository.

Converts between the Workflow Definition ORM aggregate and the domain aggregate,
including its owned Operation Definitions. Does not manage transactions.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.workflow_definition_orm import (
    OperationDefinitionORM,
    WorkflowDefinitionORM,
)
from backend.modules.laboratory.domain.aggregates.workflow_definition import (
    WorkflowDefinition,
)
from backend.modules.laboratory.domain.entities.operation_definition import (
    OperationDefinition,
)


class WorkflowDefinitionRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, workflow: WorkflowDefinition) -> None:
        self.session.add(self._to_orm(workflow))

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        orm = self.session.get(WorkflowDefinitionORM, workflow_id)
        return self._to_domain(orm) if orm else None

    def list(self) -> list[WorkflowDefinition]:
        stmt = select(WorkflowDefinitionORM).order_by(WorkflowDefinitionORM.created_at)
        return [self._to_domain(o) for o in self.session.scalars(stmt).all()]

    @staticmethod
    def _to_orm(workflow: WorkflowDefinition) -> WorkflowDefinitionORM:
        return WorkflowDefinitionORM(
            id=workflow.id,
            workflow_code=workflow.workflow_code,
            name=workflow.name,
            active=workflow.active,
            operations=[
                OperationDefinitionORM(
                    id=op.id,
                    operation_type=op.operation_type,
                    duration=op.duration,
                    required_capability=op.required_capability,
                    required_skill=op.required_skill,
                    required_qualification=op.required_qualification,
                    depends_on=list(op.depends_on),
                )
                for op in workflow.operations
            ],
        )

    @staticmethod
    def _to_domain(orm: WorkflowDefinitionORM) -> WorkflowDefinition:
        return WorkflowDefinition(
            id=orm.id,
            workflow_code=orm.workflow_code,
            name=orm.name,
            active=orm.active,
            operations=[
                OperationDefinition(
                    id=op.id,
                    operation_type=op.operation_type,
                    duration=op.duration,
                    required_capability=op.required_capability,
                    required_skill=op.required_skill,
                    required_qualification=op.required_qualification,
                    depends_on=tuple(op.depends_on or ()),
                )
                for op in orm.operations
            ],
        )
