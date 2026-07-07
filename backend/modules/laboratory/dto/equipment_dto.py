"""Equipment DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.laboratory.domain.entities.equipment import Equipment


@dataclass(slots=True)
class CreateEquipmentRequest:
    equipment_code: str
    name: str
    capabilities: set[str] = field(default_factory=set)

    @classmethod
    def from_json(cls, data: dict) -> CreateEquipmentRequest:
        return cls(
            equipment_code=data.get("equipmentCode", ""),
            name=data.get("name", ""),
            capabilities=set(data.get("capabilities", [])),
        )


def equipment_to_dict(equipment: Equipment) -> dict:
    return {
        "id": equipment.id,
        "equipmentCode": equipment.equipment_code,
        "name": equipment.name,
        "capabilities": sorted(equipment.capabilities),
        "active": equipment.active,
    }
