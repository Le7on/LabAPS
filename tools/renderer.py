from __future__ import annotations


class TemplateRenderer:
    def render(
        self,
        template: str,
        context: dict[str, str],
    ) -> str:

        result = template

        for key, value in context.items():
            result = result.replace(
                "{{" + key + "}}",
                str(value),
            )

        return result
