# ADR-017 — Skill Is Project Qualification; Remove Shift Master Data

**Status:** Accepted

**Date:** 2026-07-11

---

# Context

Staff carried two overlapping competency concepts: a free-text `skills` list
(which actually drove scheduling, matched against a method's `required_skill`)
and a Staff↔Project "qualified projects" link from ADR-014 (which the UI showed
but scheduling ignored). This was redundant and confusing (see the Gap Analysis,
2026-07-11).

Separately, the Shift master-data table (ADR-015) had no runtime consumer: the
calendar mapping (ADR-016) uses hardcoded windows per shift mode, and method
durations are plain integers. It was an isolated CRUD with a page in the nav.

The user asked to make the Staff "Skill" field a multi-select of Projects, merge
it with the existing qualified-projects link, and remove the Shift table.

---

# Decision

**1. Skill = the set of Projects a staff member is qualified for.**

- Remove `Staff.skills` (free-text) and `Staff.qualifications` (expiring map).
- The single competency is `qualified_project_ids` (API `qualifiedProjectIds`),
  surfaced in the UI as **Skill** (a checkbox multi-select of Project items).
- No expiry: a staff member is either qualified for a Project or not (the
  expiring-qualification concept is dropped).

**2. Scheduling matches staff by the method's workflow Project.**

- A method belongs to a workflow, which belongs to a Project. The operation
  instance records that Project as `required_project_id`.
- A staff member is eligible for a method when the method's project is among the
  staff's qualified projects. Implemented with the existing attribute-matching
  solver via a project token (`p:<projectId>`) — no solver change.
- Method `required_skill` / `required_qualification` are removed.

**3. Remove the Shift master-data table** (entity, ORM, DTO, repository, use
cases, API, UI, nav) and drop the `shift` table. The calendar's fixed per-mode
windows (ADR-016) are unaffected.

---

# Rationale

- One competency concept removes the redundancy and the trap where the field the
  user edited (`skills`) and the field the UI emphasised (`projectIds`) were
  different things.
- Matching by the workflow's Project matches the domain: staff are qualified per
  project (SSOT §13 examples FV / OPA / PNG), and a workflow is defined for a
  project (ADR-015).
- Dropping the unused Shift table removes dead weight and a misleading nav entry;
  nothing consumed it.
- The project-token technique keeps the scheduling engine untouched (ADR-005).

---

# Alternatives Considered

## Option A — Keep both fields (rejected)

Retain free-text skills and qualified projects. Rejected: redundant, and the two
would keep drifting.

## Option B — Keep expiry on project qualification (considered, deferred)

Model `{project_id: expiry}` so a qualification can lapse. Deferred by user
decision: expiry is dropped for now; can be reintroduced if operationally needed.

## Option C — Skill = qualified projects, no expiry, match by workflow project (chosen)

Accepted. Simplest single-concept model that satisfies the request.

---

# Consequences

Positive

- Single, unambiguous Staff competency; UI Skill field is the project multi-select.
- Scheduling staff-eligibility is project-based and matches the workflow model.
- Shift dead code removed; smaller surface.

Negative

- Breaking change: `Staff.skills`/`qualifications` and method
  `requiredSkill`/`requiredQualification` are gone; API keys changed to
  `qualifiedProjectIds`. Tests and data updated.
- Loss of granularity: eligibility is per-project, not per-skill within a
  project. If finer control is needed later, a sub-project skill concept can be
  added.
- Expiry behaviour from the old qualifications is gone.

---

# Architectural Impact

- Domain: `Staff` keeps only `qualified_project_ids`; `OperationDefinition`
  drops capability/skill/qualification.
- ORM: `staff` drops `skills`/`qualifications`; `operation_definition` drops the
  three match columns; `operation_instance` drops them and adds
  `required_project_id`; the `shift` table is dropped. Migration `d4f5061728a9`.
- Application: `generate_workflow_instance` snapshots `qualifiedProjectIds` and
  records the workflow project on each instance; `schedule_instances` matches
  staff by project token. Shift use cases/API removed.
- Frontend: StaffView Skill = project multi-select (qualifications editor and
  free-text skills removed); Workflow method rows drop skill/qualification;
  ShiftsView + route + nav removed.

---

# Related Documents

- Gap Analysis & Improvement Plan (2026-07-11)
- SSOT §11, §13 (Skill / Staff) — revised by this ADR
- ADR-014 (Staff-Project qualification — now the sole competency)
- ADR-015 (Workflow Methods — Shift master data introduced there is removed here)
- ADR-016 (Shift Calendar Mapping — unaffected; uses fixed per-mode windows)
