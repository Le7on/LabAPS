# docs/10_State_Model/02_Plan_State.md

# State Model

## Chapter 2 - Plan State Machine

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the lifecycle of the **Plan** business object.

Unlike a Plan Version, a Plan represents the long-lived business identity of a planning period.

A Plan is **not** a scheduling result.

A Plan is **not** an execution object.

Therefore its lifecycle is intentionally simple.

---

# 2. Design Philosophy

A Plan answers one question:

> "What planning identity does this planning activity belong to?"

Examples

- Week 32 Production Plan
- Week 33 Production Plan
- August Production Plan

Scheduling activities occur inside Plan Versions.

The Plan itself remains stable.

---

# 3. Lifecycle

The Plan lifecycle is intentionally minimal.

```text id="ps001"
Active

↓

Archived
```

No additional states are defined.

---

# 4. Active

## Meaning

The Plan is available for planning activities.

An Active Plan may contain:

- Working Plan Versions
- Published Plan Versions
- Historical Plan Versions

An Active Plan is the normal operating state.

---

## Allowed Actions

Users may:

- Create Plan Version
- View Versions
- Compare Versions
- Archive Plan

---

## Forbidden Actions

Users shall not:

- Delete the Plan
- Change the Planning Horizon
- Change the Plan Identity

These attributes are immutable after creation.

---

# 5. Archived

## Meaning

The planning period has ended.

The Plan becomes historical.

All Plan Versions become read-only.

---

## Allowed Actions

Users may:

- View
- Export
- Report
- Compare

---

## Forbidden Actions

Users shall not:

- Create new Plan Versions
- Publish new versions
- Modify metadata

Archived Plans are immutable.

---

# 6. State Transition

```text id="ps002"
Active

↓

Archive

↓

Archived
```

The transition is irreversible.

---

# 7. Transition Trigger

Only one business action changes Plan state.

```text id="ps003"
Archive Plan
```

Archiving may occur:

- manually
- automatically after retention policy (future)

---

# 8. Business Rules

BR-P-001

A Plan is created in the Active state.

---

BR-P-002

A Plan may own multiple Plan Versions.

---

BR-P-003

Archiving a Plan does not delete historical planning data.

---

BR-P-004

A Plan shall always preserve its business identity.

---

BR-P-005

Planning Horizon is immutable after Plan creation.

---

# 9. Relationship to Plan Version

Plan owns Plan Versions.

The lifecycle of Plan and Plan Version are independent.

Example

```text id="ps004"
Plan

Active

│

├── Version 1 (Archived)

├── Version 2 (Published)

└── Version 3 (Working)
```

The Plan remains Active while its versions evolve independently.

---

# 10. UI Behaviour

Active Plan

Available actions

- Open
- Create Version
- Archive

Archived Plan

Available actions

- View
- Export

Unavailable actions

- Create Version
- Publish

---

# 11. API Behaviour

Attempting to create a new Plan Version for an Archived Plan shall return:

```text id="ps005"
409 Conflict

PLAN_ARCHIVED
```

---

# 12. Domain Behaviour

The Plan Aggregate exposes the following business methods.

```text id="ps006"
create_version()

archive()

published_version()

latest_version()
```

The Plan Aggregate does **not** expose scheduling methods.

Scheduling belongs to Plan Version.

---

# 13. Design Decision

The Plan lifecycle intentionally remains simple.

Scheduling complexity is delegated to Plan Version.

This separation keeps:

- Aggregate responsibilities clear
- UI simpler
- API cleaner
- Domain model easier to understand

---

# 14. Related Documents

- ADR-001 — Plan as the Aggregate Root
- ADR-002 — Plan + Plan Version
- SAD Chapter 8 — Plan Lifecycle
- State Model — Plan Version State Machine
