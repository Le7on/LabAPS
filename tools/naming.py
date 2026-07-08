"""Name conversion helpers for code generation.

Generators accept a single human name (e.g. "plan version" or "PlanVersion")
and derive the casings needed by templates: snake_case, PascalCase, camelCase and
a spaced Title form.
"""

from __future__ import annotations

import re

_SPLIT = re.compile(r"[\s_\-]+|(?<=[a-z0-9])(?=[A-Z])")


def _words(name: str) -> list[str]:
    parts = [p for p in _SPLIT.split(name.strip()) if p]
    return [p.lower() for p in parts]


def to_snake(name: str) -> str:
    return "_".join(_words(name))


def to_pascal(name: str) -> str:
    return "".join(word.capitalize() for word in _words(name))


def to_camel(name: str) -> str:
    words = _words(name)
    if not words:
        return ""
    return words[0] + "".join(word.capitalize() for word in words[1:])


def to_title(name: str) -> str:
    return " ".join(word.capitalize() for word in _words(name))


def naming_context(name: str) -> dict[str, str]:
    """Build the standard {{...}} substitution context for a name."""
    return {
        "NAME_SNAKE": to_snake(name),
        "NAME_PASCAL": to_pascal(name),
        "NAME_CAMEL": to_camel(name),
        "NAME_TITLE": to_title(name),
    }
