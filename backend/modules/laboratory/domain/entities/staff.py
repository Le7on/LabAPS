"""Staff entity.

A laboratory operator with a skill set. Pure Python domain object in the
Laboratory Definition domain (separate from Planning, ADR-010). Staff owns Skills
(Business Object Model section 13); skills are the input the scheduler matches
against for Qualification/Skill constraints.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class Staff:
    staff_code: str
    name: str
    skills: set[str] = field(default_factory=set)
    # Qualifications map a qualification name to its expiry date (ISO date string,
    # or None for no expiry). A qualification is valid on/after its record until
    # (and including) the expiry date. Unlike a skill, a qualification can lapse.
    qualifications: dict[str, str | None] = field(default_factory=dict)
    # Availability windows [start, end); empty means always available (Calendar).
    availability: list[tuple[int, int]] = field(default_factory=list)
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.staff_code:
            raise ValidationError("staffCode is required")
        if not self.name:
            raise ValidationError("name is required")
        for start, end in self.availability:
            if end <= start:
                raise ValidationError("availability window end must be after start")

    def has_skill(self, skill: str) -> bool:
        return skill in self.skills

    def valid_qualifications(self, reference_date: str) -> set[str]:
        """Qualifications not expired as of ``reference_date`` (ISO date string).

        A qualification with no expiry is always valid; otherwise it is valid
        while ``reference_date <= expiry`` (lexicographic ISO date compare).
        """
        valid = set()
        for name, expiry in self.qualifications.items():
            if expiry is None or reference_date <= expiry:
                valid.add(name)
        return valid

    def deactivate(self) -> None:
        self.active = False
