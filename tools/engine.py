import sys

from context import BootstrapContext
from manifest_loader import ManifestLoader
from constants import MANIFEST_FILE
from writer import FileWriter
from renderer import TemplateRenderer



class BootstrapEngine:

    def __init__(self):

        self.context = BootstrapContext()

        self.loader = ManifestLoader(MANIFEST_FILE)

        self.writer = FileWriter()

        self.renderer = TemplateRenderer()

    def initialize(self):

        print("=" * 60)
        print("Lab APS Bootstrap")
        print("=" * 60)

        try:

            manifest = self.loader.load()
        except Exception as ex:

            print()

            print("=" * 60)

            print("Manifest Error")

            print("=" * 60)

            print(ex)

            return 1

        self.create_directories(manifest)

        self.create_packages(manifest)

        self.render_templates(manifest)

        print()

        print("Project initialized")

        return 0

    def verify(self):

        print("=" * 60)
        print("Lab APS Verify")
        print("=" * 60)
        print()

        try:
            manifest = self.loader.load()
        except Exception as ex:
            print("Manifest Error")
            print(ex)
            return 1

        missing = []

        for directory in manifest["directories"]:
            path = self.context.project_root / directory
            if not path.is_dir():
                missing.append(directory)

        for package in manifest.get("packages", []):
            init = self.context.project_root / package / "__init__.py"
            if not init.is_file():
                missing.append(f"{package}/__init__.py")

        for item in manifest["templates"]:
            target = self.context.project_root / item["target"]
            if not target.exists():
                missing.append(item["target"])

        if missing:
            print("Missing artifacts:")
            print()
            for entry in missing:
                print(f"[MISSING] {entry}")
            print()
            print(f"Verification failed ({len(missing)} missing).")
            return 1

        print("All directories, packages and files are present.")
        print()
        print("Verification passed.")
        return 0

    def doctor(self):

        print("=" * 60)
        print("Lab APS Doctor")
        print("=" * 60)
        print()

        ok = True

        version = sys.version_info
        print(
            f"[CHECK] Python {version.major}.{version.minor}.{version.micro}"
        )
        if version < (3, 11):
            print("        Python 3.11 or newer is required.")
            ok = False

        for module in ("yaml",):
            try:
                __import__(module)
                print(f"[CHECK] module '{module}' available")
            except ImportError:
                print(f"[FAIL ] module '{module}' not installed")
                ok = False

        manifest_ok = self.loader.manifest.is_file()
        print(
            f"[CHECK] manifest present: {manifest_ok}"
        )
        ok = ok and manifest_ok

        print()

        if ok:
            print("Environment OK")
            return 0

        print("Environment has issues. See checks above.")
        return 1

    def clean(self):

        print("Nothing to clean.")

    def create_directories(self, manifest):

        print()

        print("Creating directories...")

        print()

        for directory in manifest["directories"]:

            path = self.context.project_root / directory

            self.writer.mkdir(path)

            print(f"[DIR ] {directory}")

    def create_packages(self, manifest):
        
        print()

        print("Creating python packages...")

        print()

        for package in manifest.get("packages", []):

            path = self.context.project_root / package

            self.writer.mkdir(path)

            init = path / "__init__.py"

            self.writer.write_text(

                init,

                "",

                overwrite=False,

            )

    def render_templates(self, manifest):

        print()

        print("Rendering templates...")

        print()

        for item in manifest["templates"]:

            source = (
                self.context.template_root
                / item["source"]
            )

            target = (
                self.context.project_root
                / item["target"]
            )

            template = source.read_text(
                encoding="utf-8"
            )

            content = self.renderer.render(
                template,
                {
                    "PROJECT_NAME": self.context.project_name,
                    "VERSION": "1.0.0",
                },
            )

            self.writer.write_text(
                target,
                content,
                overwrite=False,
            )