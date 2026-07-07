import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_create_and_list_plan(client):
    response = client.post(
        "/api/v1/plans",
        json={
            "planningHorizon": "2026-W32",
            "name": "Week 32 Production Plan",
            "description": "Routine production",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["name"] == "Week 32 Production Plan"
    assert payload["planningHorizon"] == "2026-W32"

    listing = client.get("/api/v1/plans")
    assert listing.status_code == 200
    data = listing.get_json()
    assert data["count"] == 1
    assert data["items"][0]["name"] == "Week 32 Production Plan"


def test_get_plan_returns_details(client):
    created = client.post(
        "/api/v1/plans",
        json={
            "planningHorizon": "2026-W33",
            "name": "Week 33 Production Plan",
            "description": "Routine production",
        },
    )
    plan_id = created.get_json()["id"]

    response = client.get(f"/api/v1/plans/{plan_id}")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["id"] == plan_id
    assert payload["planCode"] == "PLAN-2026-W33"
