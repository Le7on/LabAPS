"""{{NAME_TITLE}} entity.

Domain entity for the {{NAME_TITLE}} module. Pure Python: no framework
dependencies. Protects invariants and exposes behaviour through methods.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from backend.shared.errors import ValidationError


@dataclass(slots=True)
class {{NAME_PASCAL}}:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.name:
            raise ValidationError("name is required")
