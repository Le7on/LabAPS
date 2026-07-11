"""Workflow Definition repository.

Converts between the Workflow Definition ORM aggregate and the domain aggregate,
including its owned Operation Definitions. Does not manage transactions.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.equipment_orm import EquipmentORM
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

    def get_operation(self, operation_id: str) -> OperationDefinitionORM | None:
        """Fetch a single Method (operation definition) by id, or None."""
        return self.session.get(OperationDefinitionORM, operation_id)

    def list(self) -> list[WorkflowDefinition]:
        stmt = select(WorkflowDefinitionORM).order_by(WorkflowDefinitionORM.created_at)
        return [self._to_domain(o) for o in self.session.scalars(stmt).all()]

    def count_for_project(self, project_id: str) -> int:
        stmt = select(WorkflowDefinitionORM).where(WorkflowDefinitionORM.project_id == project_id)
        return len(self.session.scalars(stmt).all())

    def delete(self, workflow_id: str) -> bool:
        orm = self.session.get(WorkflowDefinitionORM, workflow_id)
        if orm is None:
            return False
        self.session.delete(orm)
        return True

    def _to_orm(self, workflow: WorkflowDefinition) -> WorkflowDefinitionORM:
        # Resolve all bound equipment ids referenced by any method in one query.
        wanted = {eid for op in workflow.operations for eid in op.equipment_ids}
        by_id = {}
        if wanted:
            by_id = {
                e.id: e
                for e in self.session.scalars(
                    select(EquipmentORM).where(EquipmentORM.id.in_(wanted))
                ).all()
            }
        return WorkflowDefinitionORM(
            id=workflow.id,
            workflow_code=workflow.workflow_code,
            name=workflow.name,
            project_id=workflow.project_id,
            active=workflow.active,
            operations=[
                OperationDefinitionORM(
                    id=op.id,
                    operation_type=op.operation_type,
                    duration=op.duration,
                    gelatin_type=op.gelatin_type,
                    depends_on=list(op.depends_on),
                    equipment=[by_id[eid] for eid in op.equipment_ids if eid in by_id],
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
            project_id=orm.project_id,
            active=orm.active,
            operations=[
                OperationDefinition(
                    id=op.id,
                    operation_type=op.operation_type,
                    duration=op.duration,
                    gelatin_type=op.gelatin_type,
                    equipment_ids=tuple(e.id for e in op.equipment),
                    depends_on=tuple(op.depends_on or ()),
                )
                for op in orm.operations
            ],
        )
