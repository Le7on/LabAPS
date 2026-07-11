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
        self, plan_version_id: str, workflow, context: dict, run_counts: dict | None = None
    ) -> WorkflowInstanceORM:
        """Generate a workflow instance (with operation instances) and snapshot.

        Replaces any existing instances/context for the version. Each Method
        (operation) is materialized ``run_counts[method_id]`` times (default 1),
        so a plan can require a method to run multiple times. Dependencies (the
        method DAG) are preserved: run *r* of a method depends on run *r* of each
        of its prerequisite methods.
        """
        self._clear_version(plan_version_id)
        run_counts = run_counts or {}

        instance = WorkflowInstanceORM(
            plan_version_id=plan_version_id,
            workflow_definition_id=workflow.id,
            workflow_code=workflow.workflow_code,
            status="generated",
        )

        # depends_on holds prerequisite method (operation) types; map to ids.
        id_by_type = {op.operation_type: op.id for op in workflow.operations}

        seq = 0
        for op in workflow.operations:
            runs = max(1, int(run_counts.get(op.id, 1)))
            for r in range(1, runs + 1):
                seq += 1
                instance.operations.append(
                    OperationInstanceORM(
                        id=self._instance_id(op.id, r),
                        operation_definition_id=op.id,
                        operation_code=f"{workflow.workflow_code}-{op.operation_type}-{r}",
                        sequence_no=seq,
                        duration_shift=op.duration,
                        required_project_id=workflow.project_id,
                        equipment_ids=list(op.equipment_ids),
                        # Run r depends on run r of each prerequisite method.
                        depends_on=[
                            self._instance_id(id_by_type[dep], r)
                            for dep in op.depends_on
                            if dep in id_by_type
                        ],
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

    @staticmethod
    def _instance_id(method_id: str, run: int) -> str:
        """Deterministic instance id for run *r* of a method (stable within a
        generation, so dependency references resolve without a lookup table)."""
        return f"{method_id}#r{run}"

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
                "requiredProjectId": o.required_project_id,
                "equipmentIds": list(o.equipment_ids or []),
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
