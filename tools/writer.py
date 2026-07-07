from __future__ import annotations

from pathlib import Path


class FileWriter:

    def mkdir(self, path: Path):

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write_text(
        self,
        path: Path,
        content: str,
        overwrite: bool = False,
    ):

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if path.exists() and not overwrite:

            print(f"[SKIP ] {path}")

            return

        path.write_text(
            content,
            encoding="utf-8",
        )

        print(f"[WRITE] {path}")