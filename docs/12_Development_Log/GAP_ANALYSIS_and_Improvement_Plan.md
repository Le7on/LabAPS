# Gap Analysis & Improvement Plan

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Date:** 2026-07-11

**Status:** Implemented (2026-07-11) — see the Outcome section below and ADR-017.

---

## 1. Purpose

This document re-examines the current project state after the recent additions
(ADR-014 Staff-Project qualification, ADR-015 Workflow Methods/Equipment/Shifts,
ADR-016 Shift Calendar Mapping) and the user's new intent for the Staff page. It
records the defects and inconsistencies found and proposes a concrete improvement
plan. Implementation is deferred to a later round.

Ground truth below was verified against the code, not assumed.

---

## 2. User intent captured this round

1. **Staff "Skill" field → multi-select dropdown of Projects.** On the Staff
   page, Skill should be a dropdown whose options are the Project items, with
   checkboxes allowing multiple selections.
2. **Skill and "qualified projects" are the same concept — merge them.** The
   free-text skills field should be removed; there is one project-based
   multi-select, named Skill.
3. **Remove the Shift master-data entity.** The shift windows the calendar uses
   are hardcoded by mode and do not depend on the Shift table.

---

## 3. Current state (verified)

### 3.1 Staff has TWO overlapping competency concepts

- `Staff.skills` — a free-text string set. **This is what scheduling matches.**
  - Snapshotted at generation: `generate_workflow_instance.py` builds the staff
    snapshot with `"skills": sorted(s.skills)`.
  - Matched at scheduling: `schedule_instances.py` sets a staff resource's
    `provides = frozenset(s["skills"]) | valid_qualifications`, which the solver
    matches against a method's `required_skill`.
- `Staff.project_ids` — a Staff↔Project many-to-many ("qualified projects",
  ADR-014). **This does not participate in scheduling at all.** It is stored,
  returned in the API, and shown in the UI as a project multi-select, but no
  scheduling code reads it.

Result: the UI already has a project multi-select (`projectIds`) that looks like
what the user is asking for, plus a separate free-text `skills` box that is the
one actually driving the scheduler. This is the core redundancy to resolve.

### 3.2 Shift master data is an isolated CRUD with no consumers

- Files: `shift.py` (entity), `shift_orm.py`, `shift_dto.py`,
  `shift_repository.py`, `manage_shifts.py`, `shift_api.py`; wired in
  `unit_of_work.py`, `set_resource_active.py`, `database.py`, `app.py`; UI
  `ShiftsView.vue` + router + nav + store/api; test `test_shift_method_api.py`
  (the shift-master part).
- The calendar mapping (ADR-016, `engines/planning/calendar.py`) uses **hardcoded
  windows per `shift_mode`** (single 09:00-17:00; double 06:00-14:00/14:00-22:00).
  It does **not** read the Shift table.
- Method durations are "number of shifts" (an integer), also independent of the
  Shift table.

Conclusion: the Shift master-data table has no runtime consumer. Removing it is
low-risk and self-contained.

### 3.3 Documentation drift

- `IMPLEMENTATION_STATUS.md` / release-readiness notes (dated ~07-08) still list
  shift/calendar scheduling as "future work", but ADR-014/015/016 (07-10/11)
  delivered project qualification, method/equipment binding, and calendar
  mapping. The status docs are stale.
- The ADR traceability table referenced in status docs stops at ADR-013;
  ADR-014/015/016 are not reflected.
- SSOT `05_Business_Object_Model.md` §13 (Skill) still describes skills in the
  older free-text sense, while §11 + ADR-014 describe Skill as a per-Project
  qualification. The two coexist and now contradict the intended single concept.

---

## 4. Defects and inconsistencies

| #   | Severity | Area        | Defect                                                                                                                                                                                                                                     |
| --- | -------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| D1  | High     | Domain/UI   | Staff has two competency fields (`skills` free-text vs `projectIds`); the scheduler uses `skills`, the UI emphasises `projectIds`. Redundant and confusing.                                                                                |
| D2  | High     | Scheduling  | If Skill becomes "qualified Projects", scheduling must match a method's project against staff's qualified projects — but methods currently carry `required_skill` (a string), not a project reference. The matching key must be redefined. |
| D3  | Medium   | Master data | Shift table is dead weight: full CRUD + UI + nav with no consumer. Maintenance and cognitive cost, misleads users into thinking it configures the calendar.                                                                                |
| D4  | Medium   | Docs        | IMPLEMENTATION_STATUS / release-readiness are stale (pre ADR-014/015/016); ADR table stops at 013.                                                                                                                                         |
| D5  | Medium   | SSOT        | §13 Skill definition contradicts the "Skill = Project qualification" model; no single source of truth for what Skill means.                                                                                                                |
| D6  | Low      | UX          | The Workflow method row still exposes `requiredSkill` as a free-text box; after the Skill/Project merge this should reference a Project (or be derived from the workflow's project), not a free string.                                    |
| D7  | Low      | Consistency | `operation_definition.required_capability` is retained but unused after ADR-015 (equipment binding replaced it). Dead field.                                                                                                               |

---

## 5. Proposed target model (Skill = Project qualification)

Single competency concept on Staff:

- **Staff.skills becomes "qualified projects": a set of Project references.**
  Remove the free-text `skills` field; keep one project-based multi-select
  (the current `project_ids`), surfaced on the Staff page as **Skill** (a
  checkbox multi-select of Project items).
- **Scheduling matches on Project.** A method belongs to a workflow, which
  belongs to a Project. A staff member is eligible for a method when that
  Project is among the staff's qualified projects. The method's `required_skill`
  string is replaced by the workflow's Project as the staff-matching key.
- **Qualifications (expiring certifications) stay as-is** — they are a separate,
  time-bounded concept and still gate assignment.

This collapses D1 and resolves D2 with one matching rule: staff eligible ⇔
method's project ∈ staff's qualified projects (and required qualification valid).

---

## 6. Improvement plan (phased; implementation deferred)

### Phase A — Staff Skill/Project merge (addresses D1, D2, D6)

Per the Section 7 decisions:

1. Domain: drop `Staff.skills` (free-text) and the separate `qualifications`
   map; keep a single competency renamed `qualified_project_ids`. If expiry is
   kept (Section 7.1 Option 2), model it as `{project_id: expiry|None}` instead
   of a plain set.
2. Scheduling: change the staff-matching key from the `required_skill` string to
   the workflow's `project_id`. In the snapshot a staff member "provides" its
   qualified project ids (expired ones excluded if Option 2); a method requires
   its workflow's project id.
3. Method definition: drop `required_skill` and `required_qualification`
   free-text (staff eligibility now comes from the workflow's Project).
4. API/DTO: Staff exposes `qualifiedProjectIds` (replacing `skills` and
   `projectIds`); Workflow method input drops `requiredSkill` /
   `requiredQualification`.
5. Frontend StaffView: remove the free-text Skill input and the separate
   qualifications editor; the project multi-select IS the Skill field, labelled
   **Skill** (checkbox multi-select of Project items).
6. Migration + update affected tests.

### Phase B — Remove Shift master data (addresses D3)

1. Delete Shift entity/ORM/DTO/repo/use case/API; unregister blueprint; remove
   from unit_of_work, set_resource_active, database imports.
2. Delete ShiftsView, its route, nav entry, store/api functions.
3. Drop the `shift` table via a new migration (keep the calendar's hardcoded
   windows, which are unaffected).
4. Remove the shift-master portion of `test_shift_method_api.py`.
5. Confirm calendar mapping (ADR-016) and method durations still pass.

### Phase C — Documentation realignment (addresses D4, D5, D7)

1. Update IMPLEMENTATION_STATUS / release-readiness to reflect ADR-014/015/016.
2. Extend the ADR traceability table to ADR-016.
3. Rewrite SSOT §13 (Skill) to the single "Skill = Project qualification"
   definition; reconcile §11.
4. Mark `required_capability` as removed/deprecated (D7) and update SSOT §8.
5. Supersede the Shift parts of ADR-015 / SSOT §11a with a note that the Shift
   master-data table was removed (calendar uses fixed per-mode windows).

### Phase ordering & risk

- A and B are independent; B is lower risk (isolated). Recommend B first (quick
  cleanup), then A (touches scheduling — needs careful test updates), then C.
- Each phase must keep the full backend suite green and the frontend building.

---

## 7. Decisions confirmed by the user (2026-07-11)

These are settled and drive the next implementation round:

1. **Staff matching key = the workflow's Project.** A staff member can perform a
   method when the method's workflow Project is among the staff's qualified
   projects. No per-method project field is needed.
2. **Rename the field.** The merged competency field is renamed to
   `qualifiedProjectIds` (API + UI), replacing both the old free-text `skills`
   and the previous `projectIds` key. Surfaced on the Staff page as **Skill**
   (a checkbox multi-select of Project items).
3. **Qualifications are folded into Skill.** The separate expiring
   `qualifications` map on Staff is removed as an independent field and merged
   into the single project-based competency.

### 7.1 Consequence of folding qualifications in (to resolve next round)

Qualifications today are a `name → expiry date` map with expiry logic; Skill is
a set of Project references with no expiry. Folding them together forces a
choice, to be decided when Phase A is planned:

- **Option 1 (simplest):** drop expiry entirely — Skill is just the set of
  qualified Projects; a staff member is either qualified for a Project or not.
- **Option 2 (preserve expiry):** make the Staff↔Project qualification carry an
  optional expiry date, so a project qualification can lapse (keeps the
  time-bounded behaviour the old qualifications had, now keyed by Project).

Recommendation: Option 2 if expiry matters operationally; otherwise Option 1.
This must be settled before Phase A implementation.

---

## 8. Summary

The recent features work, but two structural issues remain: Staff carries two
competing competency fields (only the free-text one drives scheduling), and the
Shift master-data table is dead weight. The user's request — make Skill a
Project multi-select and remove Shift — aligns with collapsing these. This plan
merges Staff competency into a single Project-based Skill (re-pointing the
scheduler's staff matching to Project), removes the unused Shift table, and
realigns the drifted documentation.

---

## 9. Outcome (implemented 2026-07-11, ADR-017)

Decision on Section 7.1: **Option 1 — expiry dropped.** Skill is the set of
qualified Projects, no expiry.

Delivered:

- **Phase A** — `Staff.skills` and `Staff.qualifications` removed; single
  `qualifiedProjectIds` competency (UI label "Skill", a Project multi-select).
  Scheduling now matches staff by the method's workflow Project via a project
  token; method `requiredSkill`/`requiredQualification` removed.
- **Phase B** — Shift master data removed (entity/ORM/DTO/repo/use case/API, UI
  view, route, nav, store/api); `shift` table dropped. Calendar (ADR-016)
  unaffected.
- **Phase C** — SSOT §11a/§12/§13 updated; ADR-015 marked partially superseded;
  ADR-017 recorded.
- Migration `d4f5061728a9`. Backend suite: 111 passing. Frontend builds clean.

D7 (`required_capability`) is resolved: the method column was removed. The
engine's generic `Operation.required_capability`/`required_skill` fields remain
as the neutral matching mechanism (now carrying equipment and project tokens).
