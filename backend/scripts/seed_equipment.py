"""Seed the standard SU-HM equipment (idempotent).

Creates the six standard machines if they are not already present. Safe to run
repeatedly. Usage:

    python -m backend.scripts.seed_equipment
"""

from __future__ import annotations

from backend.bootstrap.container import build_container
from backend.config.settings import load_config
from backend.modules.laboratory.domain.entities.equipment import Equipment

CODES = ["SU-HM-01", "SU-HM-02", "SU-HM-09", "SU-HM-10", "SU-HM-12", "SU-HM-13"]


def seed() -> list[str]:
    container = build_container(load_config())
    container.database.create_all()

    created = []
    with container.unit_of_work() as uow:
        existing = {e.equipment_code for e in uow.equipment.list()}
        for code in CODES:
            if code in existing:
                continue
            uow.equipment.add(Equipment(equipment_code=code, name=code))
            created.append(code)
    return created


def main() -> None:
    created = seed()
    if created:
        print(f"Created equipment: {', '.join(created)}")
    else:
        print("All SU-HM equipment already present; nothing to do.")


if __name__ == "__main__":
    main()
