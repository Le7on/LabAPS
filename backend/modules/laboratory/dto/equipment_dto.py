"""Equipment DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.laboratory.domain.entities.equipment import Equipment


@dataclass(slots=True)
class CreateEquipmentRequest:
    equipment_code: str
    name: str
    availability: list[tuple[int, int]] = field(default_factory=list)
    applicable_project_ids: set[str] = field(default_factory=set)
    method_ids: set[str] = field(default_factory=set)

    @classmethod
    def from_json(cls, data: dict) -> CreateEquipmentRequest:
        return cls(
            equipment_code=data.get("equipmentCode", ""),
            name=data.get("name", ""),
            availability=[tuple(w) for w in data.get("availability", [])],
            applicable_project_ids=set(data.get("applicableProjectIds", [])),
            method_ids=set(data.get("methodIds", [])),
        )


def equipment_to_dict(equipment: Equipment) -> dict:
    return {
        "id": equipment.id,
        "equipmentCode": equipment.equipment_code,
        "name": equipment.name,
        "availability": [list(w) for w in equipment.availability],
        "applicableProjectIds": sorted(equipment.applicable_project_ids),
        "methodIds": sorted(equipment.method_ids),
        "active": equipment.active,
    }
