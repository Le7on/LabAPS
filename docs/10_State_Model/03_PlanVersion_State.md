# docs/10_State_Model/03_PlanVersion_State.md

# State Model

## Chapter 3 - Plan Version State Machine

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the lifecycle of a Plan Version.

A Plan Version represents one complete planning result.

Every planning activity—including scheduling, review and publication—is performed against a Plan Version.

Unlike the Plan, the Plan Version has a rich business lifecycle.

---

# 2. Design Philosophy

A Plan Version represents one attempt to solve a planning problem.

Examples

* Initial planning
* Re-planning after equipment maintenance
* Re-planning after demand changes
* Simulation

Every scheduling execution creates or updates one working Plan Version until it is published.

---

# 3. Lifecycle

The lifecycle is intentionally linear.

```text id="pvs001"
Working

↓

Scheduled

↓

Reviewed

↓

Published

↓

Archived
```

Each state has one clear business meaning.

---

# 4. Working

## Meaning

The planner is preparing the Plan Version.

The planner may:

* Edit Demand
* Refresh Planning Context
* Modify planning parameters

No schedule has been accepted yet.

---

## Allowed Actions

* Edit Demand
* Generate Schedule
* Delete Working Version (optional)
* Archive Version

---

## Forbidden Actions

* Publish

---

# 5. Scheduled

## Meaning

The Scheduling Engine has completed successfully.

The version now contains:

* Assignments
* Material Forecast
* KPI

The planner has not yet approved the result.

---

## Allowed Actions

* Review Schedule
* Generate Schedule Again
* Compare Versions
* Archive Version

---

## Forbidden Actions

* Execute

Execution is only allowed after publication.

---

# 6. Reviewed

## Meaning

The planner has completed manual review.

The schedule is considered acceptable.

The version is ready for publication.

---

## Typical Review Checklist

* Equipment allocation
* Staff allocation
* Material forecast
* Warnings
* KPI

---

## Allowed Actions

* Publish
* Generate Schedule Again
* Compare Versions

---

# 7. Published

## Meaning

The Plan Version becomes the official production schedule.

Only one Published Plan Version may exist within a Plan.

---

## Effects

Publishing shall:

* Lock the Plan Version
* Make Assignments executable
* Replace any previously published version

---

## Allowed Actions

* View
* Export
* Compare

---

## Forbidden Actions

* Edit Demand
* Generate Schedule
* Modify Assignments

Published versions are immutable.

---

# 8. Archived

## Meaning

Historical planning record.

The version remains available for:

* Audit
* Reporting
* Comparison

No further business actions are permitted.

---

# 9. State Transition Diagram

```text id="pvs002"
Working

│

├──────────────┐

▼              │

Scheduled      │

│              │

▼              │

Reviewed       │

│              │

▼              │

Published      │

│              │

▼              │

Archived
```

Re-running the Solver does **not** create a new state.

Instead, it regenerates the Working Version or creates a new Plan Version according to business policy.

---

# 10. Transition Rules

| Current   | Action            | Next      |
| --------- | ----------------- | --------- |
| Working   | Generate Schedule | Scheduled |
| Scheduled | Review            | Reviewed  |
| Scheduled | Generate Schedule | Scheduled |
| Reviewed  | Generate Schedule | Scheduled |
| Reviewed  | Publish           | Published |
| Working   | Archive           | Archived  |
| Scheduled | Archive           | Archived  |
| Reviewed  | Archive           | Archived  |
| Published | Archive           | Archived  |

Any other transition is invalid.

---

# 11. Invalid Transitions

Examples

```text id="pvs003"
Working

↓

Published
```

Rejected.

Reason

Schedule has not been generated or reviewed.

---

```text id="pvs004"
Published

↓

Working
```

Rejected.

Published versions are immutable.

---

```text id="pvs005"
Archived

↓

Reviewed
```

Rejected.

Archived versions are historical records.

---

# 12. Business Rules

BR-PV-001

A new Plan Version is always created in the Working state.

---

BR-PV-002

Scheduling changes the state to Scheduled only when a feasible solution is produced.

---

BR-PV-003

Only Reviewed versions may be Published.

---

BR-PV-004

Only one Published version may exist within the same Plan.

---

BR-PV-005

Published versions are immutable.

---

BR-PV-006

Archived versions remain available for reporting.

---

# 13. UI Behaviour

The user interface shall enable actions according to the current state.

| Action            | Working | Scheduled | Reviewed | Published | Archived |
| ----------------- | :-----: | :-------: | :------: | :-------: | :------: |
| Edit Demand       |    ✓    |     ✗     |     ✗    |     ✗     |     ✗    |
| Generate Schedule |    ✓    |     ✓     |     ✓    |     ✗     |     ✗    |
| Review            |    ✗    |     ✓     |     ✗    |     ✗     |     ✗    |
| Publish           |    ✗    |     ✗     |     ✓    |     ✗     |     ✗    |
| Compare           |    ✓    |     ✓     |     ✓    |     ✓     |     ✓    |
| Export            |    ✗    |     ✓     |     ✓    |     ✓     |     ✓    |
| Archive           |    ✓    |     ✓     |     ✓    |     ✓     |     ✗    |

---

# 14. API Behaviour

The API shall reject invalid business actions.

Examples

Attempting to publish a Working version:

```text id="pvs006"
409 Conflict

INVALID_PLAN_VERSION_STATE
```

Attempting to regenerate a Published version:

```text id="pvs007"
409 Conflict

PLAN_VERSION_PUBLISHED
```

---

# 15. Domain Behaviour

The PlanVersion entity exposes explicit business methods.

```text id="pvs008"
generate_schedule()

mark_reviewed()

publish()

archive()
```

Business state transitions shall occur only through these methods.

Direct modification of the status property is prohibited.

---

# 16. Domain Events

Successful transitions produce Domain Events.

Examples

```text id="pvs009"
ScheduleGenerated

PlanVersionReviewed

PlanVersionPublished

PlanVersionArchived
```

These events support:

* Audit
* Notification
* Reporting
* Future integration

---

# 17. Architectural Rules

1. Plan Version owns the planning lifecycle.

2. Scheduling never modifies a Published version.

3. Every business action validates the current state.

4. State transitions occur only inside the Domain Layer.

5. Published versions remain immutable.

6. Historical versions are append-only.

7. State changes always generate audit records.

---

# 18. Related Documents

* State Model — Plan State
* SAD Chapter 8 — Plan Lifecycle
* ADR-001 — Plan as the Aggregate Root
* ADR-002 — Plan + Plan Version
* Planning API — Publish Plan Version
