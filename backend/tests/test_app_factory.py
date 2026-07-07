"""Tests for the application factory and framework bootstrap (M1.2)."""

from __future__ import annotations

import pytest

from backend.app import create_app
from backend.config.settings import AppConfig


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_create_app_returns_configured_app():
    app = create_app()
    assert app is not None
    assert isinstance(app.config["APP_CONFIG"], AppConfig)
    assert app.config["CONTAINER"] is not None


def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["app"]
    assert payload["version"]


def test_unknown_route_returns_json_404(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    payload = response.get_json()
    assert payload["error"] == "not_found"
