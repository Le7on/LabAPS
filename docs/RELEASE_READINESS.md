# docs/RELEASE_READINESS.md

# Lab APS Release Readiness (v1.0)

**Last Updated:** 2026-07-08

This is the go/no-go checklist and readiness summary for the first release. It
complements [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) (detailed build
state) with a release-oriented view.

---

# 1. Capability Completeness

| Area                                                                                            | State |
| ----------------------------------------------------------------------------------------------- | ----- |
| Bootstrap / CLI / code generators                                                               | Done  |
| Backend framework + infrastructure (UoW, Alembic)                                               | Done  |
| Identity: token auth + roles (backend + SPA login)                                              | Done  |
| Laboratory: equipment, staff, projects, workflow definitions                                    | Done  |
| Resource availability + staff qualifications                                                    | Done  |
| Planning: plan + version lifecycle (immutability enforced)                                      | Done  |
| Demand (priority-weighted)                                                                      | Done  |
| Instances + immutable Planning Context snapshot                                                 | Done  |
| Scheduling engine (OR-Tools CP-SAT)                                                             | Done  |
| Constraints: dependency, capability, skill, resource, calendar, qualification, policy           | Done  |
| Objective: makespan / demand-weighted completion                                                | Done  |
| Assignments persisted; execution lifecycle + audit trail                                        | Done  |
| Reporting: dashboard + KPI/utilization                                                          | Done  |
| Frontend SPA: dashboard, plans, projects, equipment, staff, workflows, scheduling, Gantt, login | Done  |
| Desktop packaging (PyWebView)                                                                   | Done  |

---

# 2. Quality Gates

- Automated tests: full backend + tools suite green, including an end-to-end
  acceptance test covering the entire pipeline with authentication on.
- Static analysis: Ruff (backend/tools) and ESLint + Prettier (frontend) clean.
- Frontend build: `vite build` succeeds.
- Database: Alembic migration chain builds the full schema from empty.
- API contract: unified envelope (ADR-012) enforced; auth errors included.

---

# 3. How to Run

Development:

```text
# Backend API (dev)
.venv/Scripts/python run.py

# Frontend (dev, proxies /api to the backend)
cd frontend && npm run dev
```

Desktop:

```text
cd frontend && npm run build
python desktop.py            # opens a PyWebView window (or serves on :5000)
```

Authentication: set `AUTH_ENABLED=true` and issue a token by creating a user
(bootstrap an administrator via the auth service / a seeded token), then sign in
through the SPA login screen.

---

# 4. Known Limitations (documented, not blocking)

- Scheduling time is in integer horizon units; a real calendar/time model
  (dates, shifts, time-of-day) is future work.
- Availability/qualifications are entered directly on resources; dedicated
  shift/holiday and qualification-catalogue entities are future.
- Utilization is a busy-time proxy (no capacity denominator until calendars).
- No frozen single-file installer yet (desktop entry runs from source).
- Field editing is limited to activate/deactivate; full rename/edit is future.
- Periodic policies (e.g. "FV every 14 days") are not modelled.

---

# 5. Go / No-Go

Go for an internal v1.0 (single-user desktop / internal web). The full planning
-> scheduling -> execution -> reporting loop works end to end, is authenticated,
tested, and documented. The limitations above are enhancements, not correctness
gaps.
