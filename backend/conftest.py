"""Root test configuration.

Business tests exercise domain and API behaviour, not authentication, so auth is
disabled by default for the test session (ADR-013 auth is verified by dedicated
tests that enable it explicitly). Individual tests may re-enable it by setting
AUTH_ENABLED before creating the app.
"""

from __future__ import annotations

import os

os.environ.setdefault("AUTH_ENABLED", "false")
