"""Code generators for the Lab APS Developer CLI.

Generates module skeletons, domain entities and use cases from the templates in
``tools/templates/codegen``, following the documented implementation templates
(Module First structure, Domain Entity Template, Use Case Template).

The generator never overwrites existing files (it skips them), so it is safe to
re-run.
"""

from __future__ import annotations

from context import BootstrapContext
from naming import naming_context, to_snake
from renderer import TemplateRenderer
from writer import FileWriter

# Layers created for a new business module (Engineering Baseline: Module First).
MODULE_LAYERS = ["api", "application", "domain", "repository", "dto", "tests"]

# Domain sub-packages created inside a module.
DOMAIN_SUBPACKAGES = ["aggregates", "entities", "enums"]


class Generator:
    def __init__(self):
        self.context = BootstrapContext()
        self.writer = FileWriter()
        self.renderer = TemplateRenderer()

    # -- helpers ---------------------------------------------------------

    def _codegen_root(self):
        return self.context.template_root / "codegen"

    def _render_to(self, template_rel: str, target, ctx: dict[str, str]) -> None:
        template = (self._codegen_root() / template_rel).read_text(encoding="utf-8")
        self.writer.write_text(target, self.renderer.render(template, ctx), overwrite=False)

    def _package(self, path) -> None:
        self.writer.mkdir(path)
        self.writer.write_text(path / "__init__.py", "", overwrite=False)

    # -- generators ------------------------------------------------------

    def new_module(self, name: str) -> int:
        snake = to_snake(name)
        ctx = naming_context(name)
        module_root = self.context.project_root / "backend" / "modules" / snake

        print(f"Generating module '{snake}'...")
        print()

        self._package(module_root)
        for layer in MODULE_LAYERS:
            self._package(module_root / layer)
        for sub in DOMAIN_SUBPACKAGES:
            self._package(module_root / "domain" / sub)

        self._render_to(
            "module/entity.py.tpl",
            module_root / "domain" / "entities" / f"{snake}.py",
            ctx,
        )
        self._render_to(
            "module/repository.py.tpl", module_root / "repository" / f"{snake}_repository.py", ctx
        )
        self._render_to("module/api.py.tpl", module_root / "api" / f"{snake}_api.py", ctx)
        self._render_to("module/test.py.tpl", module_root / "tests" / f"test_{snake}.py", ctx)

        print()
        print(f"Module '{snake}' generated. Register its blueprint in backend/app.py.")
        return 0

    def new_entity(self, module: str, name: str) -> int:
        module_snake = to_snake(module)
        snake = to_snake(name)
        ctx = naming_context(name)
        target = (
            self.context.project_root
            / "backend"
            / "modules"
            / module_snake
            / "domain"
            / "entities"
            / f"{snake}.py"
        )

        print(f"Generating entity '{ctx['NAME_PASCAL']}' in module '{module_snake}'...")
        self._render_to("entity.py.tpl", target, ctx)
        return 0

    def new_usecase(self, module: str, name: str) -> int:
        module_snake = to_snake(module)
        snake = to_snake(name)
        ctx = naming_context(name)
        target = (
            self.context.project_root
            / "backend"
            / "modules"
            / module_snake
            / "application"
            / f"{snake}.py"
        )

        print(f"Generating use case '{ctx['NAME_PASCAL']}UseCase' in module '{module_snake}'...")
        self._render_to("usecase.py.tpl", target, ctx)
        return 0
