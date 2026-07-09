"""Workflow Instance repository.

Persists generated Workflow/Operation Instances and the Planning Context snapshot
for a Plan Version, and reads operation instances back for scheduling.
"""

from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.planning.planning_context_orm import (
    PlanningContextORM,
)
from backend.infrastructure.orm.planning.workflow_instance_orm import (
    OperationInstanceORM,
    WorkflowInstanceORM,
)


class WorkflowInstanceRepository:
    def __init__(self, session: Session):
        self.session = session

    def replace_for_version(
        self, plan_version_id: str, workflow, context: dict
    ) -> WorkflowInstanceORM:
        """Generate a workflow instance (with operation instances) and snapshot.

        Replaces any existing instances/context for the version, reflecting a
        fresh generation from the given Workflow Definition aggregate.
        """
        self._clear_version(plan_version_id)

        instance = WorkflowInstanceORM(
            plan_version_id=plan_version_id,
            workflow_definition_id=workflow.id,
            workflow_code=workflow.workflow_code,
            status="generated",
        )
        for seq, op in enumerate(workflow.operations, start=1):
            instance.operations.append(
                OperationInstanceORM(
                    operation_definition_id=op.id,
                    operation_code=f"{workflow.workflow_code}-OP{seq}",
                    sequence_no=seq,
                    duration_shift=op.duration,
                    required_capability=op.required_capability,
                    required_skill=op.required_skill,
                    required_qualification=op.required_qualification,
                    depends_on=list(op.depends_on),
                    status="pending",
                )
            )
        self.session.add(instance)

        self.session.add(
            PlanningContextORM(
                plan_version_id=plan_version_id,
                equipment_snapshot=context.get("equipment", []),
                staff_snapshot=context.get("staff", []),
                solver_profile=context.get("solverProfile", {}),
            )
        )
        return instance

    def list_operation_instances(self, plan_version_id: str) -> list[dict]:
        stmt = (
            select(OperationInstanceORM)
            .join(WorkflowInstanceORM)
            .where(WorkflowInstanceORM.plan_version_id == plan_version_id)
            .order_by(OperationInstanceORM.sequence_no)
        )
        return [
            {
                "id": o.id,
                "operationCode": o.operation_code,
                "operationDefinitionId": o.operation_definition_id,
                "sequenceNo": o.sequence_no,
                "duration": o.duration_shift,
                "requiredCapability": o.required_capability,
                "requiredSkill": o.required_skill,
                "requiredQualification": o.required_qualification,
                "dependsOn": list(o.depends_on or []),
                "status": o.status,
            }
            for o in self.session.scalars(stmt).all()
        ]

    def get_context(self, plan_version_id: str) -> dict | None:
        stmt = select(PlanningContextORM).where(
            PlanningContextORM.plan_version_id == plan_version_id
        )
        ctx = self.session.scalar(stmt)
        if ctx is None:
            return None
        return {
            "equipment": ctx.equipment_snapshot,
            "staff": ctx.staff_snapshot,
            "solverProfile": ctx.solver_profile,
        }

    def _clear_version(self, plan_version_id: str) -> None:
        instances = self.session.scalars(
            select(WorkflowInstanceORM).where(
                WorkflowInstanceORM.plan_version_id == plan_version_id
            )
        ).all()
        for inst in instances:
            self.session.delete(inst)  # cascade removes operation instances
        self.session.execute(
            delete(PlanningContextORM).where(PlanningContextORM.plan_version_id == plan_version_id)
        )
