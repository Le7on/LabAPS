"""Plan DTOs.

Data transfer objects for the planning API. Field names use camelCase to match
the API contract; conversion to/from domain objects happens here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.planning.domain.aggregates.plan import Plan


@dataclass(slots=True)
class CreatePlanRequest:
    planning_horizon: str
    name: str
    description: str = ""
    start_date: str | None = None
    end_date: str | None = None
    shift_mode: str = "single"
    skipped_dates: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> CreatePlanRequest:
        return cls(
            planning_horizon=data.get("planningHorizon", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            start_date=data.get("startDate") or None,
            end_date=data.get("endDate") or None,
            shift_mode=data.get("shiftMode", "single") or "single",
            skipped_dates=list(data.get("skippedDates", [])),
        )


def plan_to_dict(plan: Plan) -> dict:
    return {
        "id": plan.id,
        "planCode": plan.plan_code,
        "planningHorizon": plan.planning_horizon,
        "name": plan.name,
        "description": plan.description,
        "status": plan.status.value,
        "versionCount": len(plan.versions),
        "startDate": plan.start_date,
        "endDate": plan.end_date,
        "shiftMode": plan.shift_mode,
        "skippedDates": list(plan.skipped_dates),
        "demandLines": [
            {
                "id": line.id,
                "workflowDefinitionId": line.workflow_definition_id,
                "rounds": line.rounds,
                "targetDate": line.target_date,
            }
            for line in plan.demand_lines
        ],
    }
