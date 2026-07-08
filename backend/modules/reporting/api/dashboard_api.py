"""Reporting REST API — Dashboard.

Read-only aggregate counts. Envelope responses (ADR-012).
"""

from __future__ import annotations

from flask import Blueprint, current_app

from backend.modules.reporting.application.get_dashboard import GetDashboardUseCase
from backend.shared import api_response

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/reports/dashboard")
def get_dashboard():
    session_factory = current_app.config["CONTAINER"].session_factory
    use_case = GetDashboardUseCase(session_factory)
    return api_response.success(use_case.execute())
