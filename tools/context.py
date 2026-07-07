from dataclasses import dataclass
from pathlib import Path

from constants import (
    GENERATED_DIR,
    PROJECT_NAME,
    PROJECT_ROOT,
    TEMPLATE_DIR,
)


@dataclass(slots=True)
class BootstrapContext:
    project_name: str = PROJECT_NAME

    project_root: Path = PROJECT_ROOT

    template_root: Path = TEMPLATE_DIR

    generated_root: Path = GENERATED_DIR

    overwrite: bool = False
