# ADR-014 — Staff / Project Qualification

**Status:** Accepted

**Date:** 2026-07-10

---

# Context

The Business Object Model defines a Skill as an operator's qualification to work
on a Project (section 13, examples FV / OPA / PNG). Until now Staff carried only
a free-text `skills` list and had no explicit link to the Projects they are
qualified for; the Staff object model even stated "Staff never stores Project".

Master data setup needs to record which Projects each Staff member is qualified
for, so later planning steps can tell who may perform a given Project's work.

This ADR covers only the Staff↔Project qualification link. Deeper structure
raised in discussion — a Project owning multiple Workflows, a Workflow owning
Methods that select equipment (with a GelatinType attribute), and stages costed
in shifts — is intentionally out of scope here and will be addressed separately.

---

# Decision

Add a **Staff ↔ Project many-to-many** association: a Staff member is qualified
for zero or more Projects.

- Persisted via a `staff_project` join table.
- Exposed on the Staff API as `projectIds` (create + list).
- Creating Staff with an unknown project id is rejected (ValidationError).
- The link is Master Data competency information; it does not make Staff part of
  a Plan, and it does not (yet) change scheduling behaviour.

---

# Rationale

- Matches the SSOT definition of Skill as a per-Project qualification.
- A simple join table keeps Staff and Project as independent Master Data
  aggregates while recording the competency link.
- Keeping scheduling untouched limits blast radius; the qualification data can be
  consumed by planning later without reworking this link.

---

# Alternatives Considered

## Option A — Keep free-text skills only (rejected)

Continue encoding qualifications as arbitrary strings. Rejected: no referential
integrity to actual Projects, and no structured way to answer "who is qualified
for Project X".

## Option B — Staff belongs to a single Project (rejected)

Too restrictive: an operator is commonly qualified for several Projects.

## Option C — Staff ↔ Project many-to-many (chosen)

Accepted. Records real qualification breadth with referential integrity.

---

# Consequences

Positive

- Structured record of which Projects each Staff member may work on.
- Referential integrity: qualifications reference real Projects.

Negative

- One more relationship to maintain when Projects or Staff change.
- Does not yet feed scheduling; that is deliberate and deferred.

---

# Architectural Impact

- ORM: `staff_project` join table; `StaffORM.projects` relationship. Alembic
  migration `a1c2e3f40506`.
- Domain: `Staff.project_ids`.
- Application: `CreateStaffUseCase` validates referenced Projects exist.
- API/DTO: `projectIds` on staff create + list.
- Frontend: "Qualified for projects" multi-select on the Staff form and a
  column on the Staff table.

---

# Related Documents

- Business Object Model (SSOT sections 11, 13) — Staff section revised by this ADR
- ADR-010 (Laboratory Definition vs Planning domains)
