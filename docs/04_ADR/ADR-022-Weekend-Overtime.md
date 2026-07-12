# ADR-022 — Weekend / Holiday Overtime (per resource)

**Status:** Accepted

**Date:** 2026-07-12

---

# Context

Weekends (and holidays) are non-working by default (ADR-016/021 — no slots). But
a specific staff member or machine may occasionally work a weekend/holiday
("overtime"). This must be settable per resource and honored by scheduling.

---

# Decision

Each resource (Staff, Equipment) carries `overtime_dates`: weekend/holiday days
it is explicitly available on. At schedule time:

- The unified calendar adds every resource's overtime dates as extra working
  days (`build_calendar(extra_workdays=...)`), so those days get slots.
- A day that is only present because of overtime (a weekend or a holiday) is
  workable **only** by a resource that signed up for it: each resource's
  available windows block overtime-only days it did not sign up for, in addition
  to its own unavailable days.

UI: the availability month calendar shows weekends in purple (non-working);
clicking a weekend toggles overtime (solid purple = working). Weekday clicks
still toggle leave/maintenance (red).

---

# Consequences

Positive

- Weekend/holiday work is possible when needed, controlled per resource.
- Default behavior is unchanged (weekends off unless someone signs up).

Negative

- A weekend is schedulable only if the needed machine AND a qualified operator
  both signed up for that day; otherwise that day stays infeasible.

---

# Related

- ADR-016 (shift calendar), ADR-021 (global availability), ADR-020 (demand lines).
