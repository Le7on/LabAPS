# docs/03_SAD/08_Plan_Lifecycle.md

# Software Architecture Design

## Chapter 8 - Plan Lifecycle & State Machine

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the lifecycle of a Plan.

The lifecycle specifies:

- Valid states
- State transitions
- Allowed operations
- Ownership of each transition

The lifecycle guarantees that every Plan follows the same business process.

---

# 2. Lifecycle Overview

A Plan progresses through the following states.

```text id="k9ib8v"
Draft
   │
   ▼
Validated
   │
   ▼
Scheduled
   │
   ▼
Reviewed
   │
   ▼
Published
   │
   ▼
Executing
   │
   ▼
Completed
   │
   ▼
Archived
```

State transitions are strictly controlled.

---

# 3. State Definitions

## Draft

Purpose

Initial planning stage.

Characteristics

- Demand may be edited.
- Planning Context may be regenerated.
- Workflow Instances may be regenerated.

Assignments do not yet exist.

---

## Validated

Purpose

All planning prerequisites have passed validation.

Validation includes:

- Staff availability
- Equipment availability
- Workflow completeness
- Calendar
- Qualification

The Plan is ready for scheduling.

---

## Scheduled

Purpose

Scheduling has completed successfully.

Assignments exist.

Material Forecast and KPI are generated.

The planner may still regenerate the schedule.

---

## Reviewed

Purpose

Planner has reviewed the generated schedule.

The review includes:

- Resource allocation
- Material forecast
- Planning warnings

The Plan is awaiting publication.

---

## Published

Purpose

The Plan becomes the official execution plan.

Characteristics

- Assignments are frozen.
- Workflow structure cannot change.
- Demand cannot change.

Execution may begin.

---

## Executing

Purpose

At least one Assignment has started.

Actual execution status is recorded.

Planning information remains read-only.

---

## Completed

Purpose

All Assignments have finished.

Execution statistics are finalized.

KPIs become historical records.

---

## Archived

Purpose

Historical storage.

Archived Plans are read-only.

No further modifications are allowed.

---

# 4. State Transition Diagram

```text id="e4q4z8"
Draft
 │
 ├──────────────┐
 ▼              │
Validated       │
 │              │
 ▼              │
Scheduled       │
 │              │
 ▼              │
Reviewed        │
 │              │
 ▼              │
Published       │
 │              │
 ▼              │
Executing       │
 │              │
 ▼              │
Completed       │
 │              │
 ▼              │
Archived        │
```

Backward transitions are not allowed.

Replanning is handled through Plan Versioning.

---

# 5. Allowed Operations

| Operation         | Draft | Validated | Scheduled | Reviewed | Published | Executing | Completed |
| ----------------- | :---: | :-------: | :-------: | :------: | :-------: | :-------: | :-------: |
| Edit Demand       |   ✓   |     ✓     |     ✗     |    ✗     |     ✗     |     ✗     |     ✗     |
| Validate          |   ✓   |     ✓     |     ✗     |    ✗     |     ✗     |     ✗     |     ✗     |
| Generate Workflow |   ✓   |     ✓     |     ✗     |    ✗     |     ✗     |     ✗     |     ✗     |
| Run Solver        |   ✓   |     ✓     |     ✓     |    ✓     |     ✗     |     ✗     |     ✗     |
| Review Result     |   ✗   |     ✗     |     ✓     |    ✓     |     ✗     |     ✗     |     ✗     |
| Publish           |   ✗   |     ✗     |     ✗     |    ✓     |     ✗     |     ✗     |     ✗     |
| Update Execution  |   ✗   |     ✗     |     ✗     |    ✗     |     ✓     |     ✓     |     ✗     |
| Archive           |   ✗   |     ✗     |     ✗     |    ✗     |     ✗     |     ✓     |     ✓     |

---

# 6. Plan Version Strategy

A planning period may contain multiple Plan Versions.

Example

```text id="6r31h2"
Week 32

├── V1 Initial Plan
├── V2 Equipment Maintenance
└── V3 Demand Change
```

Rules

- Only one version may be Published.
- Older versions remain available.
- Versions are immutable after publication.

---

# 7. Replanning

A Published Plan is never modified.

If replanning is required:

```text id="y7aj2d"
Published Plan

↓

Create New Version

↓

Copy Planning Context

↓

Modify Demand

↓

Generate New Schedule

↓

Review

↓

Publish
```

The original version remains unchanged.

---

# 8. Ownership

| Action            | Responsible                   |
| ----------------- | ----------------------------- |
| Create Plan       | Production Laboratory Manager |
| Validate Plan     | System                        |
| Generate Workflow | System                        |
| Run Scheduling    | System                        |
| Review            | Production Laboratory Manager |
| Publish           | Production Laboratory Manager |
| Update Execution  | Operator                      |
| Archive           | System                        |

---

# 9. Domain Events

The following business events are generated during the lifecycle.

- PlanCreated
- PlanValidated
- ScheduleGenerated
- PlanReviewed
- PlanPublished
- ExecutionStarted
- PlanCompleted
- PlanArchived

Version 1.0 records these events for audit purposes.

Future versions may publish them asynchronously.

---

# 10. Architectural Rules

1. A Plan is always in exactly one state.

2. State transitions must follow the defined lifecycle.

3. Published Plans are immutable.

4. Replanning always creates a new Plan Version.

5. Execution never changes planning decisions.

6. Planning and execution histories must remain traceable.

7. Every Assignment belongs to exactly one Plan Version.

8. All state transitions shall be recorded in the audit log.
