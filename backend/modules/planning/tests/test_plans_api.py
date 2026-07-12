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
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "planningHorizon": "2026-W32",
            "name": "Week 32 Production Plan",
            "description": "Routine production",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["name"] == "Week 32 Production Plan"
    assert payload["data"]["planningHorizon"] == "2026-W32"

    listing = client.get("/api/v1/plans")
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["success"] is True
    assert body["meta"]["total"] == 1
    assert body["data"][0]["name"] == "Week 32 Production Plan"


def test_get_plan_returns_details(client):
    created = client.post(
        "/api/v1/plans",
        json={
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "planningHorizon": "2026-W33",
            "name": "Week 33 Production Plan",
            "description": "Routine production",
        },
    )
    plan_id = created.get_json()["data"]["id"]

    response = client.get(f"/api/v1/plans/{plan_id}")

    assert response.status_code == 200
    payload = response.get_json()["data"]
    assert payload["id"] == plan_id
    assert payload["planCode"] == "PLAN-2026-W33"


def _make_plan(client):
    return client.post(
        "/api/v1/plans",
        json={
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "planningHorizon": "2026-W32",
            "name": "Draft Plan",
        },
    ).get_json()["data"]["id"]


def test_delete_draft_plan(client):
    plan_id = _make_plan(client)
    resp = client.delete(f"/api/v1/plans/{plan_id}")
    assert resp.status_code == 200
    assert client.get("/api/v1/plans").get_json()["meta"]["total"] == 0


def test_delete_missing_plan_is_404(client):
    assert client.delete("/api/v1/plans/nope").status_code == 404


def test_cannot_delete_non_draft_plan(client):
    # Plans are Draft on creation; a non-draft plan is rejected by the guard.
    from backend.modules.planning.domain.aggregates.plan import Plan
    from backend.modules.planning.domain.enums.plan_enums import PlanStatus

    container = client.application.config["CONTAINER"]
    plan = Plan(
        planning_horizon="2026-W40",
        name="Active",
        start_date="2026-08-10",
        end_date="2026-08-20",
        status=PlanStatus.ACTIVE,
    )
    with container.unit_of_work() as uow:
        uow.plans.add(plan)

    resp = client.delete(f"/api/v1/plans/{plan.id}")
    assert resp.status_code == 409
