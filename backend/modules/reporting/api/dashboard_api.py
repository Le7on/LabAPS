"""Reporting REST API — Dashboard.

Read-only aggregate counts. Envelope responses (ADR-012).
"""

from __future__ import annotations

from flask import Blueprint, current_app

from backend.modules.reporting.application.get_dashboard import GetDashboardUseCase
from backend.modules.reporting.application.get_kpi import GetKpiUseCase
from backend.shared import api_response

dashboard_bp = Blueprint("dashboard", __name__)


def _session_factory():
    return current_app.config["CONTAINER"].session_factory


@dashboard_bp.get("/reports/dashboard")
def get_dashboard():
    return api_response.success(GetDashboardUseCase(_session_factory()).execute())


@dashboard_bp.get("/reports/kpi")
def get_kpi():
    return api_response.success(GetKpiUseCase(_session_factory()).execute())
