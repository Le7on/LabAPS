"""Staff DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.laboratory.domain.entities.staff import Staff


@dataclass(slots=True)
class CreateStaffRequest:
    staff_code: str
    name: str
    skills: set[str] = field(default_factory=set)
    availability: list[tuple[int, int]] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> CreateStaffRequest:
        return cls(
            staff_code=data.get("staffCode", ""),
            name=data.get("name", ""),
            skills=set(data.get("skills", [])),
            availability=[tuple(w) for w in data.get("availability", [])],
        )


def staff_to_dict(staff: Staff) -> dict:
    return {
        "id": staff.id,
        "staffCode": staff.staff_code,
        "name": staff.name,
        "skills": sorted(staff.skills),
        "availability": [list(w) for w in staff.availability],
        "active": staff.active,
    }
