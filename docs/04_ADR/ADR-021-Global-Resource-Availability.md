# ADR-021 — Global Per-Resource Availability

**Status:** Accepted (supersedes per-plan availability)

**Date:** 2026-07-12

---

# Context

Staff take leave and equipment goes down for maintenance; these apply across all
plans, not per plan. An earlier iteration stored availability per plan; that was
the wrong home for it and duplicated data across plans.

---

# Decision

Availability is a **global per-resource** concern. Staff and Equipment each carry
`unavailable_dates` (a list of "YYYY-MM-DD" days off). A dedicated Availability
page shows a resource list + a month calendar: days are available (green) by
default, click a day to mark it unavailable (red).

At schedule time the plan calendar's slots are masked by each resource's
unavailable dates (converted to available shift-slot windows), so a resource is
never scheduled on a day it is off. The old per-plan availability
(`plan_resource_availability`, its API/use case/repo) is removed.

---

# Consequences

Positive

- One place to manage leave / maintenance; consistent across every plan.
- Matches the real world (a person on leave is unavailable to all plans).

Negative

- No per-plan override (deemed unnecessary; a resource off is off everywhere).
- The old `plan_resource_availability` table remains in the DB but is unused.

---

# Architectural Impact

- Staff/Equipment gain `unavailable_dates` (replaces the unused integer
  `availability` windows). API: `POST /{staff|equipment}/{id}/unavailable-dates`.
- generate-instances snapshots each active resource's unavailable dates;
  schedule_instances masks the calendar accordingly.
- Frontend: dedicated Availability page (resource list + month calendar).

---

# Related

- ADR-016 (shift calendar), ADR-020 (PI plan demand lines).
