# ADR-015 — Workflow Methods, Equipment Binding and Shifts

**Status:** Accepted (partially superseded by ADR-017)

**Date:** 2026-07-10

> Superseded parts (ADR-017, 2026-07-11): the Shift master-data table introduced
> here was removed (no scheduling consumer; the calendar uses fixed per-mode
> windows, ADR-016). Method `required_skill` / `required_qualification` were also
> removed — staff eligibility is now by the workflow's Project. Method equipment
> binding and the Project→Workflow→Method structure from this ADR remain in force.

---

# Context

Master data needed a richer workflow structure. A Project owns multiple Workflow
Templates; each Workflow is composed of ordered Methods (= Stages). A Method
selects the instruments it runs on and carries a GelatinType attribute, and its
workload is measured in work shifts rather than abstract integer units.

Previously: Workflow Templates had no owning Project; steps were "Operation
Definitions" matched to equipment by a capability string; duration was an
abstract integer; there was no Shift concept (only an unused `duration_shift`
column and a "Shift Definition" mention in Planning Context).

---

# Decision

1. **Workflow → Project (N:1, required).** Every Workflow Template belongs to
   exactly one Project.
2. **Method (= Stage).** The existing Operation Definition is the Method. A
   Method adds a `gelatin_type` attribute and binds Equipment directly.
3. **Method ↔ Equipment (M:N), replacing capability matching.** A Method's
   equipment candidates are exactly the equipment bound to it. The former
   `required_capability` string match for equipment is dropped.
4. **Shift master data.** A Shift is `shift_code` + `name` + `start_time` +
   `end_time`. A Method's duration is the number of shifts it occupies, and
   **1 shift = 1 scheduler time unit**.
5. Staff matching (required skill / qualification) is unchanged.

Equipment binding is enforced without changing the solver: at problem-build time
each Method requires a synthetic token `m:<instanceId>` and each bound Equipment
provides that token, so the existing attribute-matching restricts the Method to
its bound equipment.

---

# Rationale

- Mirrors how the lab actually defines work: Project → Workflow → Method, with
  each Method pinned to specific instruments.
- Binding equipment explicitly is clearer and less error-prone than maintaining
  matching capability strings on both equipment and steps.
- Shifts give planners a domain-meaningful unit; mapping 1 shift → 1 time unit
  keeps the scheduler integer-based and unchanged.
- The synthetic-token technique keeps the OR-Tools adapter and scheduling model
  untouched (ADR-005 boundary preserved).

---

# Alternatives Considered

## Option A — Keep capability matching, add equipment binding on top (rejected)

Two overlapping mechanisms for the same decision; confusing and redundant.

## Option B — Push equipment sets into the solver as a new constraint (rejected)

Couples the engine to laboratory concepts; the token approach achieves the same
with no solver change.

## Option C — Method binds equipment; token-based restriction (chosen)

Accepted. Explicit binding, solver untouched, integer durations preserved.

---

# Consequences

Positive

- Clear Project → Workflow → Method structure with instrument binding.
- Shift-based durations are meaningful to planners; solver stays integer-based.
- No solver change; snapshot reproducibility preserved (ADR-008).

Negative

- Breaking change: workflow creation requires a Project, and methods bind
  equipment instead of declaring a capability (existing tests/data updated).
- A Method with no bound equipment has no equipment candidate; if it needs one,
  it is unassignable. This is intentional under explicit binding.
- 1 shift = 1 time unit is a simplification; shift clock times are informational
  and not yet used to place work on a real calendar.

---

# Architectural Impact

- ORM: `shift` table; `method_equipment` join; `workflow_definition.project_id`;
  `operation_definition.gelatin_type`; `operation_instance.equipment_ids`.
  Alembic migration `b2d3f5061728`.
- Domain: `Shift`; `WorkflowDefinition.project_id`; `OperationDefinition`
  gains `gelatin_type` and `equipment_ids`.
- Application: Shift CRUD use cases; workflow create validates project +
  equipment; `_build_problem` uses per-method equipment tokens.
- API/DTO: `/shifts` endpoints; workflow accepts `projectId` and per-method
  `gelatinType` / `equipmentIds`.
- Frontend: ShiftsView; Workflow form gains Project select and Method rows
  (gelatin type, equipment multi-select, shift-count duration).

---

# Related Documents

- Business Object Model (SSOT sections 6, 8, 11a) — revised by this ADR
- ADR-005 (Scheduling Model as anti-corruption layer)
- ADR-008 (Planning Context snapshots)
- ADR-014 (Staff-Project qualification)
