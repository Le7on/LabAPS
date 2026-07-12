# ADR-024 — FV Priority over PI Target Date (soft target dates)

**Status:** Accepted (refines ADR-019/020)

**Date:** 2026-07-12

---

# Context

A PI request specifies a target date. FV (equipment validation) is a hard
periodic requirement. When a request's target day is consumed by FV (or the
machine is out of validity that day), pinning the request hard to that day made
it an unschedulable conflict — even though running it a day later would be fine.
The user wants FV to take priority and the target date to give way.

---

# Decision

The PI **target date is a soft preference; FV stays a hard constraint.** A
request's rounds may start no earlier than the target date but may drift to a
later working day. The scheduler pulls each round to its earliest feasible slot
(weighted-completion objective), so it lands on the target day when possible and
on the nearest later working day when the target is taken (e.g. by FV). Only
rounds that fit nowhere in the horizon become conflicts.

Implementation:

- A round's task window is `[first slot on/after target, horizon)` instead of
  the single target day.
- schedule_plans uses the weighted-completion objective so each round is pulled
  as early as possible (closest to its target).
- FV occupancy and availability are unchanged (still hard).

---

# Consequences

Positive

- FV always happens on time; requests flow to the next available day instead of
  failing.
- Fewer spurious conflicts; conflicts now mean "no room anywhere on/after the
  target", which is actionable.

Negative

- A request may run later than its exact target date without being flagged;
  the day-grid shows where each round actually landed.
- Drift is later-only (never before the target).

---

# Related

- ADR-019 (FV validity), ADR-020 (demand lines), ADR-023 (partial scheduling).
