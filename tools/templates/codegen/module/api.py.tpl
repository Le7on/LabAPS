"""{{NAME_TITLE}} REST API.

Adapts HTTP requests to {{NAME_TITLE}} use cases. Request parsing, DTO conversion
and HTTP responses only; no business logic. Responses use the envelope contract
(ADR-012) via backend.shared.api_response.
"""

from __future__ import annotations

from flask import Blueprint, current_app

from backend.shared import api_response

{{NAME_SNAKE}}_bp = Blueprint("{{NAME_SNAKE}}", __name__)


def _container():
    return current_app.config["CONTAINER"]


@{{NAME_SNAKE}}_bp.get("/{{NAME_SNAKE}}")
def list_{{NAME_SNAKE}}():
    # Wire to a use case built from _container().unit_of_work.
    return api_response.collection([])
