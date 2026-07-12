# ADR-020 — PI Plan Demand Lines (workflow × rounds × target date)

**Status:** Accepted

**Date:** 2026-07-12

---

# Context

A Principal Investigator (PI) requests production for an upcoming period by
specifying, per workflow, how many rounds to run and on which day. Multiple PIs
may submit plans. The previous model attached demand (project quantity/priority)
to a plan _version_; it did not capture "run workflow X, N rounds, on date D" as
a hard-dated request.

---

# Decision

A **Plan owns Demand Lines**. Each line is `(workflow_definition_id, rounds,
target_date)`:

- `rounds` — how many times to run that workflow.
- `target_date` — the day those rounds must run (a hard constraint), and it must
  fall within the plan's date range.

Scheduling (ADR to follow for the multi-plan run) materializes each line into
`rounds` workflow instances pinned to `target_date`, competing for shared
resources on the calendar.

Availability moves to a **global per-resource** concern (dedicated calendar page),
superseding the earlier per-plan availability.

---

# Rationale

- Matches how PIs actually request work (per workflow, per day).
- The date is first-class and enforced, not a soft preference.
- Keeping lines on the Plan (not the version) lets several plans be selected and
  merged into one scheduling run.

---

# Consequences

Positive

- Clear, auditable PI requests; supports multiple PIs and multiple plans.
- Target-date hard constraints are explicit.

Negative

- The old version-level Demand (priority weighting) is superseded for this flow.
- If a target day lacks resource capacity, the run is infeasible (surfaced to the
  planner to resolve).

---

# Architectural Impact

- `PlanDemandLine` entity + `plan_demand_line` table (owned by Plan);
  repository/DTO/use-cases/API (`POST/DELETE /plans/{id}/demand-lines`).
- Plan page: expandable per-plan editor to add/remove request lines.

---

# Related

- ADR-016 (shift calendar), ADR-018 (equipment binding), ADR-019 (FV validity).
