"""API response envelope helpers.

Builds the unified response contract defined in ADR-012 and
08_API/04_API_Response_Standard.md:

    success: {"success": true, "data": ..., "meta": {...}}
    error:   {"success": false, "error": {code, message, details}, "meta": {...}}

Used by the API layer so every endpoint shares one outer structure.
"""

from __future__ import annotations

from typing import Any

from flask import jsonify


def success(data: Any = None, meta: dict | None = None, status: int = 200):
    """Build a success envelope response tuple ``(response, status)``."""

    body = {"success": True, "data": data, "meta": meta or {}}
    return jsonify(body), status


def collection(items: list, meta: dict | None = None, status: int = 200):
    """Build a collection envelope; pagination/count belong in ``meta``."""

    merged = {"total": len(items)}
    if meta:
        merged.update(meta)
    return success(data=items, meta=merged, status=status)


def error(code: str, message: str, status: int, details: list | None = None):
    """Build an error envelope response tuple ``(response, status)``."""

    body = {
        "success": False,
        "error": {"code": code, "message": message, "details": details or []},
        "meta": {},
    }
    return jsonify(body), status
