# ADR-016 — Shift Calendar Mapping

**Status:** Accepted

**Date:** 2026-07-11

---

# Context

The scheduler works in abstract integer time units. Users need results on a real
calendar: concrete dates and shift windows, honouring weekends/holidays. Method
durations are already expressed in shifts (ADR-015), and the assignment ORM
anticipated this ("when a calendar is modelled, the times become datetimes").

Shift patterns are fixed per plan: a single-shift day (09:00-17:00) or a
double-shift day (06:00-14:00 and 14:00-22:00). Non-working days (weekends,
holidays) are handled by letting the user skip specific dates.

---

# Decision

Add an optional **calendar configuration on the Plan**: `start_date`, `end_date`,
`shift_mode` (`single` | `double`), and `skipped_dates` (list of ISO dates).

Define the mapping as a pure function: lay out shift slots day by day from
start to end, skipping skipped dates; each remaining day contributes its
mode's slots in order. **One integer scheduler unit = one shift slot.** The
total slot count becomes the scheduler's planning horizon.

At scheduling time, when the plan has a calendar:

- The horizon is the slot count (a too-short calendar makes the problem
  infeasible — capacity is explicit).
- Each Assignment's integer `[start, end)` maps to real `startAt` / `endAt`
  datetimes and the starting slot's shift label, persisted alongside the
  integer units.

Plans without a calendar keep the plain integer behaviour unchanged.

Parallel methods sharing a time unit naturally share a shift slot, so "multiple
methods in one shift" needs no special handling.

---

# Rationale

- A pure calendar function keeps the mapping testable and the solver untouched
  (ADR-005 boundary preserved); the scheduler still sees only integers.
- Storing both integer units and datetimes keeps existing consumers (KPI
  busy-time, Gantt) working while adding calendar output.
- Fixed shift windows per mode match the stated operating model and avoid
  ambiguity (the same "Shift1" label differs between single and double days, so
  the window is derived from the mode, not a shared shift table).
- Skipped dates give weekend/holiday handling without a separate holiday
  aggregate this round.

---

# Alternatives Considered

## Option A — Frontend-only conversion (rejected)

Return integers and let the UI compute dates. Rejected: the mapping (skipped
days, capacity/infeasibility) is scheduling logic and belongs server-side; the
user asked for real dates from the backend.

## Option B — Hours as the base unit (rejected)

Make one integer unit = one hour. Rejected: methods are defined in shifts
(ADR-015); a shift-slot unit keeps durations and the calendar aligned.

## Option C — Shift-slot units mapped server-side (chosen)

Accepted. One unit = one shift slot; the backend maps to datetimes.

---

# Consequences

Positive

- Assignments carry real dates + shift labels; weekends/holidays are skippable.
- Solver and scheduling model are unchanged.
- Backward compatible: calendar-less plans behave as before.

Negative

- Horizon is bounded by calendar capacity; a short date range can make an
  otherwise-solvable plan infeasible (intentional, tested).
- Shift windows are fixed in code per mode, not configurable from the Shift
  master-data table; the two mechanisms are intentionally separate for now.
- 1 unit = 1 shift means a method cannot occupy a partial shift.

---

# Architectural Impact

- Engine: pure `backend/engines/planning/calendar.py`
  (`build_calendar`, `slot_count`, `map_interval`).
- ORM: `plan` gains `start_date`, `end_date`, `shift_mode`, `skipped_dates`;
  `assignment` gains `planned_start_at`, `planned_end_at`, `planned_shift`.
  Alembic migration `c3e4a5162839`.
- Domain: `Plan` calendar fields + `has_calendar()`.
- Application: `ScheduleInstancesUseCase` builds the calendar, sets the horizon
  from slot count, and maps assignment intervals to datetimes.
- API/DTO: plan accepts/returns `startDate` / `endDate` / `shiftMode` /
  `skippedDates`; assignments return `startAt` / `endAt` / `shift`.
- Frontend: PlansView calendar inputs (dates, shift mode, skipped dates);
  SchedulingView shows real datetimes + shift labels.

---

# Related Documents

- Business Object Model (SSOT section 4, Planning Context) — updated by this ADR
- ADR-005 (Scheduling Model as anti-corruption layer)
- ADR-008 (Planning Context snapshots)
- ADR-015 (Workflow Methods, Equipment Binding and Shifts)
