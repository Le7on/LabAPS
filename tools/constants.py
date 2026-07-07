from pathlib import Path

VERSION = "1.0.0"

PROJECT_NAME = "Lab APS"

TOOLS_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = TOOLS_DIR.parent

TEMPLATE_DIR = TOOLS_DIR / "templates"

GENERATED_DIR = TOOLS_DIR / "generated"

MANIFEST_FILE = TOOLS_DIR / "manifest.yaml"