"""Make the tools/ modules importable for tests.

The developer CLI uses flat imports (``from naming import ...``); this puts the
tools directory on sys.path so tests can import them directly.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
