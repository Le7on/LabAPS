"""Equipment DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.modules.laboratory.domain.entities.equipment import Equipment


@dataclass(slots=True)
class CreateEquipmentRequest:
    equipment_code: str
    name: str
    unavailable_dates: list[str] = field(default_factory=list)
    overtime_dates: list[str] = field(default_factory=list)
    applicable_project_ids: set[str] = field(default_factory=set)
    method_ids: set[str] = field(default_factory=set)
    fv_duration: int = 1
    fv_validity: int = 14

    @classmethod
    def from_json(cls, data: dict) -> CreateEquipmentRequest:
        return cls(
            equipment_code=data.get("equipmentCode", ""),
            name=data.get("name", ""),
            unavailable_dates=list(data.get("unavailableDates", [])),
            overtime_dates=list(data.get("overtimeDates", [])),
            applicable_project_ids=set(data.get("applicableProjectIds", [])),
            method_ids=set(data.get("methodIds", [])),
            fv_duration=int(data.get("fvDuration", 1)),
            fv_validity=int(data.get("fvValidity", 14)),
        )


def equipment_to_dict(equipment: Equipment) -> dict:
    return {
        "id": equipment.id,
        "equipmentCode": equipment.equipment_code,
        "name": equipment.name,
        "unavailableDates": list(equipment.unavailable_dates),
        "overtimeDates": list(equipment.overtime_dates),
        "applicableProjectIds": sorted(equipment.applicable_project_ids),
        "methodIds": sorted(equipment.method_ids),
        "fvDuration": equipment.fv_duration,
        "fvValidity": equipment.fv_validity,
        "active": equipment.active,
    }
