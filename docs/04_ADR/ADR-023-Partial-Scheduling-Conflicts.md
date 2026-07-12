# ADR-023 — Partial Scheduling with Conflict Reporting

**Status:** Accepted

**Date:** 2026-07-12

---

# Context

When a resource is unavailable (or a target day is over capacity), the old
behavior failed the whole run as "infeasible", giving the planner nothing. The
planner would rather see everything that _can_ be scheduled and a clear list of
what can't, to resolve it.

---

# Decision

Scheduling is **partial**: every task is optionally scheduled. The solver
maximizes the number of scheduled tasks first (each worth more than any timing
cost), then optimizes timing. A run is always feasible; tasks that cannot be
placed — no eligible/available resource, or no room given capacity/calendar —
are returned as `unscheduled` and surfaced as conflicts.

- Solver: per-task `scheduled` boolean; assignment "exactly one resource" is
  conditioned on `scheduled`; objective `big * placed - timing`.
- A required kind with no eligible resource forces `scheduled = 0`.
- Fully-unavailable resources are kept with a zero-length window (present but
  ineligible) so their requirement isn't silently dropped.
- schedule_plans maps unscheduled operation ids back to per-demand-line conflicts
  (plan, workflow·method, target date, unscheduled rounds).
- UI: a Conflicts panel lists them; the header shows "Fully scheduled" vs
  "Scheduled with conflicts".

---

# Consequences

Positive

- The planner always gets a usable partial schedule plus an actionable conflict
  list.

Negative

- "Infeasible" is no longer a status for resource/capacity shortfalls; callers
  read the conflicts list instead.

---

# Related

- ADR-019 (FV), ADR-020 (demand lines), ADR-021/022 (availability/overtime).
