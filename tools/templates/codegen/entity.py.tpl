"""{{NAME_TITLE}} entity.

Domain entity for {{NAME_TITLE}}. Pure Python: no Flask, SQLAlchemy or OR-Tools.
Protects its own invariants and exposes behaviour through methods (Domain Entity
Template, chapters 3-6). Business state is the result of behaviour, never a
public setter.
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

    # Business behaviour goes here as methods, e.g.:
    #
    #     def activate(self) -> None:
    #         ...
    #
    # Do not expose public setters; mutate state through behaviour.
