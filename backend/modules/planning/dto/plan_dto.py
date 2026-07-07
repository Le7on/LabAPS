"""Plan DTOs.

Data transfer objects for the planning API. Field names use camelCase to match
the API contract; conversion to/from domain objects happens here.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.modules.planning.domain.aggregates.plan import Plan


@dataclass(slots=True)
class CreatePlanRequest:
    planning_horizon: str
    name: str
    description: str = ""

    @classmethod
    def from_json(cls, data: dict) -> CreatePlanRequest:
        return cls(
            planning_horizon=data.get("planningHorizon", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
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
    }
