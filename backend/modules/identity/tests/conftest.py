"""Test fixtures for the identity module (isolated temp SQLite, auth enabled)."""

from __future__ import annotations

import contextlib
import os
import tempfile
from collections.abc import Iterator

import pytest


@pytest.fixture(autouse=True)
def isolated_database() -> Iterator[None]:
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)

    prev_db = os.environ.get("DATABASE_URL")
    prev_auth = os.environ.get("AUTH_ENABLED")
    os.environ["DATABASE_URL"] = f"sqlite:///{path}"
    os.environ["AUTH_ENABLED"] = "true"  # identity tests exercise the guard
    try:
        yield
    finally:
        for key, prev in (("DATABASE_URL", prev_db), ("AUTH_ENABLED", prev_auth)):
            if prev is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = prev
        with contextlib.suppress(OSError):
            os.remove(path)
