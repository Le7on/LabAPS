from __future__ import annotations

from pathlib import Path

import yaml


class ManifestError(Exception):
    """Manifest validation error."""


class ManifestLoader:
    def __init__(self, manifest: Path):
        self.manifest = manifest

    def load(self) -> dict:
        if not self.manifest.exists():
            raise ManifestError(f"Manifest not found:\n{self.manifest}")

        with self.manifest.open(
            "r",
            encoding="utf-8",
        ) as f:
            manifest = yaml.safe_load(f)

        self.validate(manifest)

        return manifest

    # --------------------------------------------------------

    def validate(
        self,
        manifest: dict,
    ):
        if not isinstance(manifest, dict):
            raise ManifestError("Manifest root must be a dictionary.")

        self._validate_list(
            manifest,
            "directories",
        )

        self._validate_list(
            manifest,
            "packages",
        )

        self._validate_list(
            manifest,
            "templates",
        )

    # --------------------------------------------------------

    @staticmethod
    def _validate_list(
        manifest: dict,
        key: str,
    ):
        value = manifest.get(key)

        if value is None:
            raise ManifestError(f"Missing '{key}' section.")

        if not isinstance(value, list):
            raise ManifestError(f"'{key}' must be a list.")
