# ADR-019 — FV (Facility/Equipment Validation) Validity Constraint

**Status:** Accepted

**Date:** 2026-07-11

---

# Context

Every piece of equipment must undergo a validation run ("FV") periodically. A
normal operation may only run on a machine while that machine's FV is **in
validity** — i.e. within a fixed window (14 days) after its most recent completed
FV. FV itself is real work: it occupies the machine for a duration.

The user requires that scheduling both:

1. **Enforce** that every operation on equipment X runs while X's FV is valid, and
2. **Automatically insert** FV runs so validity is maintained across the horizon.

Validity is tracked **per equipment** (each machine has its own FV timeline).

---

# Decision

Model FV as a **first-class, auto-generated scheduling task per equipment**, and
constrain every normal operation to lie within a validity window of its
machine's FV.

- Each equipment carries FV parameters: `fv_duration` (shifts an FV occupies) and
  `fv_validity` (shifts an FV remains valid; default 14 in day-shift units).
- At schedule time, for every equipment that any operation can run on, the engine
  generates FV tasks covering the horizon: one at the start, then repeating so
  that consecutive FVs are no more than `fv_validity` apart. FV tasks occupy the
  equipment (no overlap with normal operations, enforced by the existing resource
  constraint).
- Each normal operation assigned to equipment X must **start within the validity
  window** of some FV of X: there exists an FV `f` on X with
  `f.end <= op.start <= f.end + fv_validity`.
- FV tasks appear in the schedule/assignments like any other task (they are real
  occupancy), tagged so the UI can distinguish them.

Because generation is deterministic and periodic, the "auto-insert" and "enforce"
requirements are satisfied by the same mechanism: FVs are placed to keep validity
continuous, and operations are bound to those FVs.

---

# Rationale

- FV is genuinely equipment time, so representing it as a task (not just a date
  check) makes the schedule honest about machine occupancy.
- Per-equipment FV timelines match the requirement and keep machines independent.
- Reusing the existing resource no-overlap constraint means FV automatically
  competes for the machine with normal work — no separate mechanism.
- Deterministic periodic placement keeps the model solvable and explainable.

---

# Alternatives Considered

## A — Date check only (no FV task)

Track "last FV date" per machine and reject operations outside 14 days. Rejected:
it ignores that FV consumes machine time and cannot auto-insert FVs.

## B — Fully free FV placement (solver decides count/timing)

Let the solver choose when to run FVs. Rejected for now: adds optional-task
cardinality and validity-coverage constraints that are heavy and hard to explain;
deterministic periodic placement is sufficient and predictable.

## C — Periodic FV tasks + validity binding (chosen)

Deterministic FV tasks per equipment covering the horizon; operations bound to an
in-validity FV. Predictable, reuses existing constraints.

---

# Consequences

Positive

- Operations can never be scheduled on an out-of-validity machine.
- FV occupancy is visible and competes for the machine realistically.
- Per-equipment timelines are independent and easy to reason about.

Negative

- FV cadence is deterministic, not cost-optimized (may run an FV slightly earlier
  than strictly necessary). Acceptable; can move to Alternative B later.
- The horizon must be long enough to place at least one FV; very short horizons
  place a single FV at the start.

---

# Architectural Impact

- Equipment gains `fv_duration` and `fv_validity` attributes (default 1 and 14).
- The scheduling model gains a task `kind` marker (normal vs FV) and a
  per-task validity link; the engine builder generates FV tasks and validity
  constraints. The solver adapter enforces them with existing interval/no-overlap
  plus a "start within window of some FV" disjunction.
- Assignments flag FV rows so the UI/Gantt can label them.

---

# Related

- ADR-015 (Workflow/Method/Shift), ADR-016 (Shift Calendar), ADR-018 (per-plan
  availability). FV validity composes with the calendar and availability.
