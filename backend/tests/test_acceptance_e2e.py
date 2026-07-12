"""End-to-end acceptance test: the full Lab APS pipeline with auth enabled.

Walks the whole product flow a user would perform, exercising every module
together (identity, laboratory, planning, scheduling engine, execution,
reporting) through the REST API with authentication on.
"""

from __future__ import annotations

import contextlib
import os
import tempfile
from collections.abc import Iterator

import pytest

from backend.app import create_app
from backend.modules.identity.domain.role import Role


@pytest.fixture(autouse=True)
def isolated_database() -> Iterator[None]:
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    prev_db = os.environ.get("DATABASE_URL")
    prev_auth = os.environ.get("AUTH_ENABLED")
    os.environ["DATABASE_URL"] = f"sqlite:///{path}"
    os.environ["AUTH_ENABLED"] = "true"
    try:
        yield
    finally:
        for key, prev in (("DATABASE_URL", prev_db), ("AUTH_ENABLED", prev_auth)):
            if prev is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = prev
        with contextlib.suppress(OSError):
            os.remove(path)


def test_full_pipeline_end_to_end():
    app = create_app()
    app.config.update(TESTING=True)
    token = app.config["CONTAINER"].auth_service.create_user("lm", Role.PRODUCTION_LM)["token"]
    client = app.test_client()
    auth = {"Authorization": f"Bearer {token}"}

    def post(url, json=None):
        return client.post(url, json=json or {}, headers=auth)

    def get(url):
        return client.get(url, headers=auth)

    # 1. Laboratory setup: project, equipment, skilled+qualified staff.
    project_id = post("/api/v1/projects", {"projectCode": "PRJ-1", "name": "Assay"}).get_json()[
        "data"
    ]["id"]
    eq_id = post(
        "/api/v1/equipment",
        {"equipmentCode": "EQ-1", "name": "Cycler", "capabilities": ["pcr"]},
    ).get_json()["data"]["id"]
    post(
        "/api/v1/staff",
        {
            "staffCode": "ST-1",
            "name": "Alice",
            "qualifiedProjectIds": [project_id],
        },
    )

    # 2. Workflow (for the project) with methods bound to equipment. Staff
    #    eligibility comes from the workflow's project (ADR-017).
    workflow_id = post(
        "/api/v1/workflow-definitions",
        {
            "workflowCode": "WF-1",
            "name": "PCR run",
            "projectId": project_id,
            "operations": [
                {"operationType": "prep", "duration": 2, "equipmentIds": [eq_id]},
                {
                    "operationType": "amplify",
                    "duration": 3,
                    "equipmentIds": [eq_id],
                    "dependsOn": [],
                },
            ],
        },
    ).get_json()["data"]["id"]

    # 3. Plan + version.
    plan_id = post(
        "/api/v1/plans",
        {
            "planningHorizon": "2026-W33",
            "name": "Week 33",
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
        },
    ).get_json()["data"]["id"]
    version_id = post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"

    # 4. Demand (drives the weighted objective).
    post(base + "/demands", {"projectId": project_id, "quantity": 5, "priority": "high"})

    # 5. Generate instances + snapshot, then schedule.
    gen = post(base + "/generate-instances", {"workflowDefinitionId": workflow_id})
    assert gen.status_code == 201
    assert gen.get_json()["data"]["operationCount"] == 2

    scheduled = post(base + "/schedule-instances")
    assert scheduled.status_code == 200
    assert scheduled.get_json()["meta"]["feasible"] is True

    # 6. Lifecycle: review + publish -> assignments become Ready.
    assert post(base + "/review").status_code == 200
    assert post(base + "/publish").status_code == 200

    assignments = get(base + "/assignments").get_json()["data"]
    assert len(assignments) == 2
    assert all(a["status"] == "ready" for a in assignments)

    # 7. Execute one assignment through to completion, with an audit trail.
    aid = assignments[0]["id"]
    assert post(f"/api/v1/executions/{aid}/start").status_code == 200
    assert post(f"/api/v1/executions/{aid}/complete").status_code == 200
    history = get(f"/api/v1/executions/{aid}/history").get_json()
    assert [h["action"] for h in history["data"]] == ["start", "complete"]

    # 8. Reporting reflects the run.
    dash = get("/api/v1/reports/dashboard").get_json()["data"]
    assert dash["plans"] == 1
    assert dash["publishedVersions"] == 1
    kpi = get("/api/v1/reports/kpi").get_json()["data"]
    assert kpi["assignmentStatus"].get("completed") == 1
    assert any(u["assignmentCount"] > 0 for u in kpi["equipmentUtilization"])
