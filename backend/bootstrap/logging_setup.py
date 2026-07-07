"""Logging initialization.

Configures the root logger once during application startup. Business code
obtains loggers via ``logging.getLogger(__name__)`` and never configures logging
itself.
"""

from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DEFAULT_LOGGING_FILE = CONFIG_DIR / "logging.yaml"

_DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def init_logging(logging_file: Path | None = None) -> None:
    """Initialize logging from YAML config, falling back to a basic config."""

    path = logging_file or DEFAULT_LOGGING_FILE

    if path.is_file():
        import logging.config

        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if raw:
            logging.config.dictConfig(raw)
            return

    logging.basicConfig(level=logging.INFO, format=_DEFAULT_FORMAT)
