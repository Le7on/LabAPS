"""User roles (ADR-013).

Roles gate sensitive business actions. Kept minimal for the current stage
(Planning API security section: Production LM, Administrator).
"""

from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    ADMINISTRATOR = "administrator"
    PRODUCTION_LM = "production_lm"
