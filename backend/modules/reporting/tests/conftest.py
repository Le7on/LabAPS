"""Test fixtures for the reporting module (isolated temp SQLite per test)."""

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

    previous = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = f"sqlite:///{path}"
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = previous
        with contextlib.suppress(OSError):
            os.remove(path)
