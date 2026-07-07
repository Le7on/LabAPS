"""Equipment API tests."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_create_and_list_equipment(client):
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipmentCode": "EQ-001",
            "name": "Centrifuge",
            "capabilities": ["spin", "cool"],
        },
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["equipmentCode"] == "EQ-001"
    assert payload["capabilities"] == ["cool", "spin"]
    assert payload["active"] is True

    listing = client.get("/api/v1/equipment")
    assert listing.status_code == 200
    data = listing.get_json()
    assert data["count"] == 1
    assert data["items"][0]["name"] == "Centrifuge"


def test_create_equipment_requires_code(client):
    response = client.post("/api/v1/equipment", json={"name": "No code"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "validation_error"
