# docs/IMPLEMENTATION_STATUS.md

# Lab APS Implementation Status & Traceability

**Last Updated:** 2026-07-08

**Purpose:** A single map from architecture to code: what is implemented, where
it lives, which milestone delivered it, and how it is tested. Complements the
architecture index (design) with the current build state.

---

# 1. Phase Status

| Phase | Name                                                               | Status                     |
| ----- | ------------------------------------------------------------------ | -------------------------- |
| 1     | Bootstrap (CLI, skeleton, framework)                               | Implemented                |
| 2     | Infrastructure (SQLAlchemy, UoW, Alembic)                          | Implemented                |
| 3     | Planning Domain (Plan, Plan Version, lifecycle)                    | Implemented                |
| 4     | Scheduling Engine (OR-Tools, resources, persistence)               | Implemented                |
| 5     | Execution (assignment lifecycle)                                   | Implemented (first slice)  |
| 6     | Reporting (dashboard)                                              | Implemented (first slice)  |
| —     | Frontend SPA (dashboard, plans, laboratory, workflows, scheduling) | Implemented (first slices) |

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

| ADR     | Decision                           | Where enforced                                                           |
| ------- | ---------------------------------- | ------------------------------------------------------------------------ |
| ADR-001 | Plan as Aggregate Root             | `domain/aggregates/plan.py` (owns versions)                              |
| ADR-002 | Plan + Plan Version                | `domain/entities/plan_version.py`                                        |
| ADR-003 | Workflow Definition vs Instance    | `laboratory/domain/aggregates/workflow_definition.py`                    |
| ADR-004 | Operation Definition vs Instance   | `laboratory/domain/entities/operation_definition.py`                     |
| ADR-005 | Scheduling Model as ACL            | `engines/scheduling/*`, `solver/*` (business objects never enter solver) |
| ADR-006 | Constraint Model not direct solver | `ortools_solver_adapter` translates a framework-free model               |
| ADR-007 | Constraint vs Objective split      | constraints in adapter; objective (makespan) isolated; noted interim     |
| ADR-010 | Separate Laboratory and Planning   | distinct modules; cross-read only at application layer                   |
| ADR-011 | Vue 3 SPA                          | `frontend/`                                                              |
| ADR-012 | Unified API response envelope      | `shared/api_response.py`, `shared/error_handlers.py`                     |

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
| Qualification (expiry)  | Not yet     |
| Calendar / availability | Not yet     |
| Policy                  | Not yet     |

Objective: demand-weighted completion when a version has demand, else makespan
(ADR-007; see M11.2). Utilization/balance objectives are future.

---

# 6. REST API Surface

| Method + path                                             | Module     |
| --------------------------------------------------------- | ---------- |
| GET /api/v1/health                                        | shared     |
| POST/GET /api/v1/plans, GET /plans/{id}                   | planning   |
| POST /plans/{id}/versions                                 | planning   |
| POST /plans/{id}/versions/{vid}/schedule                  | planning   |
| POST /plans/{id}/versions/{vid}/schedule-from-workflow    | planning   |
| GET /plans/{id}/versions/{vid}/assignments                | planning   |
| POST /plans/{id}/versions/{vid}/{review,publish,archive}  | planning   |
| POST/GET /api/v1/equipment                                | laboratory |
| POST/GET /api/v1/staff                                    | laboratory |
| POST/GET /api/v1/workflow-definitions                     | laboratory |
| POST /api/v1/executions/{id}/{start,complete,fail,cancel} | execution  |
| GET /api/v1/reports/dashboard                             | reporting  |

All responses use the `{success, data, meta}` envelope (ADR-012).

---

# 7. Test & Quality Snapshot

- Backend + tools: 66 tests passing; overall coverage ~97%.
- Frontend: `vite build` succeeds (100 modules); ESLint + Prettier clean.
- Alembic: full chain creates plan, plan_version, equipment, staff,
  workflow_definition, operation_definition, assignment.
- Lint/format: Ruff (backend/tools), ESLint + Prettier (frontend), Prettier
  (Markdown) all clean.

---

# 8. Known Gaps / Next

- Project aggregate + per-operation demand attribution (Operation Instances and
  a Planning Context snapshot now exist; assignments reference instance ids).
- Calendar/qualification constraints; a real objective model once Demand exists.
- Execution history/audit records; reporting KPI and utilization.
- Domain events (documented but deferred until an event bus exists).
- Authentication/authorization (documented as future).

See per-milestone delivery docs in `12_Development_Log/` for details, and
`12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md` for the session index.
