"""Staff DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.laboratory.domain.entities.staff import Staff


@dataclass(slots=True)
class CreateStaffRequest:
    staff_code: str
    name: str
    unavailable_dates: list[str] = field(default_factory=list)
    qualified_project_ids: set[str] = field(default_factory=set)

    @classmethod
    def from_json(cls, data: dict) -> CreateStaffRequest:
        return cls(
            staff_code=data.get("staffCode", ""),
            name=data.get("name", ""),
            unavailable_dates=list(data.get("unavailableDates", [])),
            qualified_project_ids=set(data.get("qualifiedProjectIds", [])),
        )


def staff_to_dict(staff: Staff) -> dict:
    return {
        "id": staff.id,
        "staffCode": staff.staff_code,
        "name": staff.name,
        "unavailableDates": list(staff.unavailable_dates),
        "qualifiedProjectIds": sorted(staff.qualified_project_ids),
        "active": staff.active,
    }
