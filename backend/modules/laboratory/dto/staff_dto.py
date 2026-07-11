"""Staff DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.laboratory.domain.entities.staff import Staff


@dataclass(slots=True)
class CreateStaffRequest:
    staff_code: str
    name: str
    availability: list[tuple[int, int]] = field(default_factory=list)
    qualified_project_ids: set[str] = field(default_factory=set)

    @classmethod
    def from_json(cls, data: dict) -> CreateStaffRequest:
        return cls(
            staff_code=data.get("staffCode", ""),
            name=data.get("name", ""),
            availability=[tuple(w) for w in data.get("availability", [])],
            qualified_project_ids=set(data.get("qualifiedProjectIds", [])),
        )


def staff_to_dict(staff: Staff) -> dict:
    return {
        "id": staff.id,
        "staffCode": staff.staff_code,
        "name": staff.name,
        "availability": [list(w) for w in staff.availability],
        "qualifiedProjectIds": sorted(staff.qualified_project_ids),
        "active": staff.active,
    }
