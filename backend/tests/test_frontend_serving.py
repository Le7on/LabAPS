"""Tests for SPA static serving (desktop packaging).

When the frontend build exists, the app serves index.html for client routes but
never for API paths. When it is absent, no catch-all route is registered.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from backend.app import create_app

DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
HAS_BUILD = (DIST / "index.html").is_file()


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


@pytest.mark.skipif(not HAS_BUILD, reason="frontend build not present")
def test_root_serves_spa(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!doctype html>" in response.data.lower()


@pytest.mark.skipif(not HAS_BUILD, reason="frontend build not present")
def test_client_route_falls_back_to_index(client):
    response = client.get("/scheduling")
    assert response.status_code == 200


def test_unknown_api_path_is_json_404_not_spa(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    # Still the JSON error envelope, not the SPA index.
    assert response.get_json()["success"] is False
