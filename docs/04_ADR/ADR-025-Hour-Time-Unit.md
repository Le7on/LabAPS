# ADR-025 — Scheduler Time Unit in Hours (WorkHours)

**Status:** Accepted (refines ADR-016)

**Date:** 2026-07-12

---

# Context

Method WorkHours (duration) and the scheduler's time axis were measured in whole
shifts (1 integer unit = 1 shift). The smallest schedulable unit was therefore a
whole shift, which is too coarse — work is planned in hours.

---

# Decision

The scheduler's integer time unit is **one hour**. WorkHours/duration and FV
parameters are expressed in hours; the minimum granularity is 1 hour.

- The shift calendar now emits one slot per hour within each shift window:
  single shift 09:00–17:00 = 8 hourly slots; double = 16.
- Method `duration` is hours. FV `fv_duration`/`fv_validity` are hours
  (defaults: 8h occupied, valid 112h = 14×8h).
- All downstream logic (availability windows, day windows, target-date drift,
  map_interval) operates on the hourly slot list unchanged.

Existing dev data was rescaled shifts→hours (durations ×8; FV 1/14 shifts →
8/112 hours).

---

# Consequences

Positive

- Work can be planned to the hour; a shift holds multiple methods.
- The day grid still groups by day; assignment start/end map to real clock times.

Negative

- The horizon grows ~8× (more solver variables); fine at current scale.
- Values previously entered as shifts must be read as hours (dev data migrated).

---

# Related

- ADR-016 (shift calendar), ADR-019 (FV), ADR-024 (soft target dates).
