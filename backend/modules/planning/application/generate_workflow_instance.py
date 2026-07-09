"""Generate Workflow Instance use case.

Materializes a Workflow Definition into Operation Instances on a Plan Version and
captures an immutable Planning Context snapshot of the active resources
(ADR-008). This is the step that turns reusable definitions into version-owned,
schedulable instances.
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError, ValidationError


class GenerateWorkflowInstanceUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str, version_id: str, workflow_definition_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            plan.get_version(version_id)  # raises NotFoundError if missing

            workflow = uow.workflow_definitions.get(workflow_definition_id)
            if workflow is None:
                raise NotFoundError(f"Workflow definition {workflow_definition_id} not found")
            if not workflow.operations:
                raise ValidationError("Workflow definition has no operations")

            # Immutable snapshot of the resources available at generation time.
            context = {
                "equipment": [
                    {
                        "id": e.id,
                        "capabilities": sorted(e.capabilities),
                        "availability": [list(w) for w in e.availability],
                    }
                    for e in uow.equipment.list()
                    if e.active
                ],
                "staff": [
                    {
                        "id": s.id,
                        "skills": sorted(s.skills),
                        "availability": [list(w) for w in s.availability],
                    }
                    for s in uow.staff.list()
                    if s.active
                ],
                "solverProfile": {"objective": "makespan"},
            }

            instance = uow.workflow_instances.replace_for_version(version_id, workflow, context)
            result = {
                "id": instance.id,
                "planVersionId": version_id,
                "workflowDefinitionId": workflow_definition_id,
                "workflowCode": instance.workflow_code,
                "operationCount": len(instance.operations),
            }

        return result
