# docs/IMPLEMENTATION_STATUS.md

# Lab APS Implementation Status & Traceability

**Last Updated:** 2026-07-11

**Purpose:** A single map from architecture to code: what is implemented, where
it lives, which milestone delivered it, and how it is tested. Complements the
architecture index (design) with the current build state.

---

# 1. Phase Status

| Phase | Name                                                               | Status      |
| ----- | ------------------------------------------------------------------ | ----------- |
| 1     | Bootstrap (CLI, skeleton, framework)                               | Implemented |
| 2     | Infrastructure (SQLAlchemy, UoW, Alembic)                          | Implemented |
| 3     | Planning Domain (Plan, Plan Version lifecycle, Demand)             | Implemented |
| 4     | Scheduling Engine (OR-Tools; all constraint categories; objective) | Implemented |
| 5     | Execution (assignment lifecycle + audit history)                   | Implemented |
| 6     | Reporting (dashboard + KPI/utilization)                            | Implemented |
| 7     | Identity (token auth + roles), Desktop packaging, Acceptance       | Implemented |
| —     | Frontend SPA (all views, Gantt, login)                             | Implemented |

Release readiness: see [RELEASE_READINESS.md](RELEASE_READINESS.md) — internal
v1.0 go.

---

# 2. Module Map

| Module         | Responsibility                                                  | Key code                      | Tests                       |
| -------------- | --------------------------------------------------------------- | ----------------------------- | --------------------------- |
| planning       | Plan aggregate, versions, scheduling orchestration, assignments | `backend/modules/planning/`   | `modules/planning/tests/`   |
| laboratory     | Equipment, Staff, Workflow/Operation Definition                 | `backend/modules/laboratory/` | `modules/laboratory/tests/` |
| execution      | Assignment execution lifecycle                                  | `backend/modules/execution/`  | `modules/execution/tests/`  |
| reporting      | Read-only dashboard (query service)                             | `backend/modules/reporting/`  | `modules/reporting/tests/`  |
| engines        | Planning problem, scheduling model/engine                       | `backend/engines/`            | `engines/tests/`            |
| solver         | OR-Tools CP-SAT adapter (isolated)                              | `backend/solver/`             | `solver/tests/`             |
| infrastructure | ORM, persistence, Unit of Work                                  | `backend/infrastructure/`     | (via module tests)          |
| tools          | Developer CLI + code generators                                 | `tools/`                      | `tools/tests/`              |

---

# 3. ADR Traceability

| ADR     | Decision                              | Where enforced                                                            |
| ------- | ------------------------------------- | ------------------------------------------------------------------------- |
| ADR-001 | Plan as Aggregate Root                | `domain/aggregates/plan.py` (owns versions)                               |
| ADR-002 | Plan + Plan Version                   | `domain/entities/plan_version.py`                                         |
| ADR-003 | Workflow Definition vs Instance       | `laboratory/domain/aggregates/workflow_definition.py`                     |
| ADR-004 | Operation Definition vs Instance      | `laboratory/domain/entities/operation_definition.py`                      |
| ADR-005 | Scheduling Model as ACL               | `engines/scheduling/*`, `solver/*` (business objects never enter solver)  |
| ADR-006 | Constraint Model not direct solver    | `ortools_solver_adapter` translates a framework-free model                |
| ADR-007 | Constraint vs Objective split         | constraints in adapter; objective (makespan / demand-weighted) selectable |
| ADR-010 | Separate Laboratory and Planning      | distinct modules; cross-read only at application layer                    |
| ADR-011 | Vue 3 SPA                             | `frontend/`                                                               |
| ADR-012 | Unified API response envelope         | `shared/api_response.py`, `shared/error_handlers.py`                      |
| ADR-013 | Token authentication + roles          | `shared/auth.py`, `modules/identity/*`                                    |
| ADR-014 | Staff-Project qualification (skill)   | `staff_orm` staff_project join; `schedule_instances` skill token          |
| ADR-015 | Workflow / Method / equipment bind    | `workflow_definition_orm`, `method_equipment` join                        |
| ADR-016 | Shift calendar mapping                | `engines/planning/calendar.py`; plan start/end/shift fields               |
| ADR-017 | Skill is project qualification        | staff `qualified_project_ids`; project token matching                     |
| ADR-018 | Equipment applicable projects/methods | `equipment_project`, `method_equipment` joins                             |
| ADR-019 | FV (equipment validation) validity    | `SchedulingResource.fv_intervals`; solver FV intervals                    |

---

# 4. State Model Traceability

| State machine                                                    | Where enforced                                          | Tests                                                 |
| ---------------------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------- |
| Plan Version (Working->Scheduled->Reviewed->Published->Archived) | `domain/entities/plan_version.py`, `aggregates/plan.py` | `test_plan_version_lifecycle*.py`                     |
| Assignment (Pending->Ready->Running->Completed/Failed/Cancelled) | `execution/domain/assignment_status.py`                 | `test_assignment_status.py`, `test_executions_api.py` |

---

# 5. Constraint Framework Coverage (Scheduling)

| Category                | Status      |
| ----------------------- | ----------- |
| Dependency (precedence) | Implemented |
| Capability (equipment)  | Implemented |
| Skill (staff)           | Implemented |
| Resource no-overlap     | Implemented |
| Qualification (expiry)  | Implemented |
| Calendar / availability | Implemented |
| Policy (frozen window)  | Implemented |
| FV validity (ADR-019)   | Implemented |
| Per-plan availability   | Implemented |

Objective: demand-weighted completion when a version has demand, else makespan
(ADR-007; see M11.2). Utilization/balance objectives are future.

FV validity (ADR-019): every equipment must be validated periodically
(`fv_validity` shifts); FV is placed as fixed per-equipment occupancy so normal
work only runs while a machine's FV is valid. Per-plan availability lets a plan
mark specific staff/equipment unavailable for its period.

---

# 6. REST API Surface

| Method + path                                                                     | Module     |
| --------------------------------------------------------------------------------- | ---------- |
| GET /api/v1/health                                                                | shared     |
| GET /api/v1/auth/whoami; POST /api/v1/users                                       | identity   |
| POST/GET /api/v1/plans; GET /plans/{id}                                           | planning   |
| POST /plans/{id}/versions                                                         | planning   |
| POST /plans/{id}/versions/{vid}/schedule (manual ops)                             | planning   |
| POST /plans/{id}/versions/{vid}/generate-instances                                | planning   |
| POST /plans/{id}/versions/{vid}/schedule-instances                                | planning   |
| POST/GET /plans/{id}/versions/{vid}/demands                                       | planning   |
| GET /plans/{id}/versions/{vid}/assignments                                        | planning   |
| POST /plans/{id}/versions/{vid}/{review,publish,archive}                          | planning   |
| GET/POST /plans/{id}/availability (per-plan resource availability)                | planning   |
| POST/GET/PUT/DELETE /api/v1/equipment; POST /equipment/{id}/{deactivate,activate} | laboratory |
| POST/GET/PUT/DELETE /api/v1/staff; POST /staff/{id}/{deactivate,activate}         | laboratory |
| POST/GET/PUT/DELETE /api/v1/projects; POST /projects/{id}/{deactivate,activate}   | laboratory |
| POST/GET /api/v1/workflow-definitions; DELETE /workflow-definitions/{id}          | laboratory |
| POST /api/v1/executions/{id}/{start,complete,fail,cancel}; GET .../history        | execution  |
| GET /api/v1/reports/dashboard; GET /api/v1/reports/kpi                            | reporting  |

All responses use the `{success, data, meta}` envelope (ADR-012).

---

# 7. Test & Quality Snapshot

- Backend + tools: 136 tests passing, including an end-to-end acceptance test
  covering the full authenticated pipeline.
- Frontend: `vite build` succeeds (117 modules); ESLint + Prettier clean.
- Alembic: full chain builds the complete schema from empty (plan, plan_version,
  demand, workflow/operation instance, planning_context, assignment, execution
  record, equipment (+fv fields), staff, project, workflow/operation definition,
  users/tokens, plan_resource_availability, and the staff/equipment/method join
  tables).
- Lint/format: Ruff (backend/tools), ESLint + Prettier (frontend), Prettier
  (Markdown) all clean.

---

# 8. Known Gaps / Next

- FV occupancy is enforced in scheduling but not yet drawn on the frontend
  timeline (assignments show, FV blocks do not).
- FV cadence is deterministic/periodic, not cost-optimized (ADR-019 alt B).
- Per-operation (vs aggregate) demand attribution.
- Utilization/balance objectives; a richer objective model.
- Domain events (documented but deferred until an event bus exists).
- FV validity is measured in shift units, not literal calendar days.

See per-milestone delivery docs in `12_Development_Log/` for details, and
`12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md` for the session index.
