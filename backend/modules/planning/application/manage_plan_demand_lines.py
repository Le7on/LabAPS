"""Plan demand-line use cases (ADR-020).

A PI adds request lines to a plan: run a workflow N rounds on a target date.
"""

from __future__ import annotations

from backend.modules.planning.domain.entities.plan_demand_line import PlanDemandLine
from backend.shared.errors import NotFoundError, ValidationError


class AddPlanDemandLineUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str, data: dict) -> dict:
        line = PlanDemandLine(
            workflow_definition_id=data.get("workflowDefinitionId", ""),
            rounds=int(data.get("rounds", 0)),
            target_date=data.get("targetDate", ""),
        )
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            if uow.workflow_definitions.get(line.workflow_definition_id) is None:
                raise ValidationError(f"Unknown workflow: {line.workflow_definition_id}")
            # The target date must fall inside the plan's calendar.
            if plan.start_date and (
                line.target_date < plan.start_date or line.target_date > plan.end_date
            ):
                raise ValidationError("targetDate must be within the plan's date range")
            plan.demand_lines.append(line)
            uow.plans.save(plan)

        return {
            "id": line.id,
            "planId": plan_id,
            "workflowDefinitionId": line.workflow_definition_id,
            "rounds": line.rounds,
            "targetDate": line.target_date,
        }


class RemovePlanDemandLineUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str, line_id: str) -> dict:
        with self._uow_factory() as uow:
            if not uow.plans.remove_demand_line(plan_id, line_id):
                raise NotFoundError("Plan or demand line not found")
        return {"id": line_id, "deleted": True}
