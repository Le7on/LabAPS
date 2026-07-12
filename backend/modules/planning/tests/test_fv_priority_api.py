"""FV priority over PI target date (ADR-024).

FV is a hard periodic constraint; a PI request's target date is a soft preference
that may drift to a later working day when the target day is taken by FV.
"""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_pi_request_drifts_past_fv_day(client):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    # FV occupies 1 shift and stays valid a long time; on a single-shift calendar
    # the FV consumes the machine's first day (2026-08-10), so a request targeting
    # that day must drift to the next working day.
    # FV occupies a full single-shift day (8h) and stays valid a long time, so
    # it consumes all of 2026-08-10; a request targeting that day must drift.
    eq_id = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "M", "fvDuration": 8, "fvValidity": 9999},
    ).get_json()["data"]["id"]
    workflow = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "SMDP",
            "name": "SMDP",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 1, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]
    method_id = workflow["operations"][0]["id"]
    client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-1", "name": "Alice", "qualifiedProjectIds": [project_id]},
    )
    # Mon 2026-08-10 .. Fri 2026-08-14 (single shift/day).
    plan_id = client.post(
        "/api/v1/plans",
        json={
            "name": "P",
            "planningHorizon": "2026-W33",
            "startDate": "2026-08-10",
            "endDate": "2026-08-14",
            "shiftMode": "single",
        },
    ).get_json()["data"]["id"]
    client.post(
        f"/api/v1/plans/{plan_id}/demand-lines",
        json={
            "workflowDefinitionId": workflow["id"],
            "operationDefinitionId": method_id,
            "rounds": 1,
            "targetDate": "2026-08-10",
        },
    )

    body = client.post("/api/v1/schedule", json={"planIds": [plan_id]}).get_json()
    assert body["meta"]["feasible"] is True
    assert body["data"]["conflicts"] == []
    # FV took 08-10; the request ran the next working day instead of conflicting.
    a = body["data"]["assignments"][0]
    assert a["startAt"][:10] == "2026-08-11"
