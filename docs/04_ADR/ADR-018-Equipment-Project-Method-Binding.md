# ADR-018 — Equipment ↔ Project / Method Binding

**Status:** Accepted

**Date:** 2026-07-08

---

# Context

Scheduling must know which equipment can run a given method. Two relationships
express this in the laboratory domain:

- An equipment is **applicable to** a set of Projects.
- An equipment is **bound to** specific Methods (operation definitions) of those
  projects' workflows.

Earlier drafts matched equipment to operations by a free-text "capability"
string. That was ambiguous (capabilities drifted from real machine/method pairs)
and could not express "this exact method runs on these exact machines".

---

# Decision

Model both relationships as explicit many-to-many joins, and let the scheduler
restrict a method to exactly its bound equipment.

- `equipment_project` join: which projects an equipment is applicable to.
- `method_equipment` join: which methods (operation definitions) an equipment can
  run.
- At schedule time, a method's equipment candidates are exactly the equipment
  bound to it (a synthetic per-method token is provided by each bound machine),
  not a capability match.

Free-text equipment capabilities were removed.

---

# Rationale

- Explicit joins are unambiguous and editable in the UI (multi-selects).
- "Method runs on these machines" is a first-class fact, not inferred from
  string overlap.
- Reusing the solver's attribute-matching (a per-method token) needs no solver
  change.

---

# Consequences

Positive

- Equipment/method eligibility is exact and maintainable.
- The UI can present real dropdowns instead of free text.

Negative

- Bindings must be maintained as workflows/methods change (mitigated by CRUD).

---

# Architectural Impact

- ORM join tables `equipment_project` and `method_equipment`
  (`orm/laboratory/associations.py`); Equipment carries `applicable_project_ids`
  and `method_ids`.
- `schedule_instances` builds per-method equipment tokens from these bindings.

---

# Related

- ADR-015 (Workflow / Method), ADR-017 (Skill is project qualification),
  ADR-019 (FV validity).
