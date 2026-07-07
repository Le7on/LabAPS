# docs/10_State_Model/05_Execution_State.md

# State Model

## Chapter 5 - Execution State Machine

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the lifecycle of an Execution.

Execution represents the actual execution of an Assignment.

Planning creates the Assignment.

Execution records reality.

Execution never changes planning decisions.

---

# 2. Design Philosophy

Assignment represents the planned schedule.

Execution represents the actual laboratory activity.

Planning answers

> What should happen?

Execution answers

> What actually happened?

These two concepts shall remain independent.

---

# 3. Relationship

```text
Plan Version

↓

Assignment

↓

Execution
```

An Assignment may have:

* zero Execution (not started)
* one active Execution
* one completed Execution

Version 1.0 supports one Execution per Assignment.

---

# 4. Lifecycle

```text
Not Started

↓

Running

├────────────► Completed

├────────────► Failed

└────────────► Cancelled
```

Execution states are runtime states.

---

# 5. Not Started

## Meaning

Execution has not begun.

The Assignment is waiting.

Actual Start Time is empty.

---

## Allowed Actions

* Start

---

## Forbidden Actions

* Complete
* Fail

---

# 6. Running

## Meaning

The laboratory work is currently executing.

Execution records:

* Actual Start Time
* Current Operator
* Current Equipment

Version 1.0 assumes the planned resources remain unchanged.

---

## Allowed Actions

* Complete
* Fail
* Cancel

---

# 7. Completed

## Meaning

Execution completed successfully.

Actual End Time is recorded.

Execution becomes read-only.

---

# 8. Failed

## Meaning

Execution terminated unsuccessfully.

Failure information shall include:

* Failure Time
* Failure Reason
* Optional Notes

Examples

* Instrument Failure
* QC Failure
* Operator Error
* Unexpected Exception

---

# 9. Cancelled

## Meaning

Execution was intentionally stopped before completion.

Examples

* Manual cancellation
* Instrument unavailable
* Plan superseded

Cancellation reason shall be recorded.

---

# 10. State Transition Diagram

```text
Not Started

↓

Running

├────────► Completed

├────────► Failed

└────────► Cancelled
```

Backward transitions are prohibited.

---

# 11. Transition Rules

| Current     | Action   | Next      |
| ----------- | -------- | --------- |
| Not Started | Start    | Running   |
| Running     | Complete | Completed |
| Running     | Fail     | Failed    |
| Running     | Cancel   | Cancelled |

All other transitions are invalid.

---

# 12. Runtime Attributes

Execution maintains runtime information.

Examples

* Actual Start Time
* Actual End Time
* Duration
* Failure Reason
* Cancellation Reason
* Execution Notes

These values never modify the Assignment.

---

# 13. Business Rules

BR-EX-001

Execution may start only when the Assignment is in the Ready state.

---

BR-EX-002

Execution records actual timestamps.

Planned timestamps remain unchanged.

---

BR-EX-003

Execution never modifies:

* Plan
* Plan Version
* Workflow Instance
* Operation Instance

---

BR-EX-004

Completed, Failed and Cancelled are terminal states.

---

# 14. UI Behaviour

| Action   | Not Started | Running | Completed | Failed | Cancelled |
| -------- | :---------: | :-----: | :-------: | :----: | :-------: |
| Start    |     ✓     |   ✗   |    ✗    |   ✗   |    ✗    |
| Complete |     ✗     |   ✓   |    ✗    |   ✗   |    ✗    |
| Fail     |     ✗     |   ✓   |    ✗    |   ✗   |    ✗    |
| Cancel   |     ✗     |   ✓   |    ✗    |   ✗   |    ✗    |
| View     |     ✓     |   ✓   |    ✓    |   ✓   |    ✓    |

---

# 15. API Behaviour

Examples

Start Execution

```http
POST /api/v1/executions/{executionId}:start
```

Complete Execution

```http
POST /api/v1/executions/{executionId}:complete
```

Fail Execution

```http
POST /api/v1/executions/{executionId}:fail
```

Cancel Execution

```http
POST /api/v1/executions/{executionId}:cancel
```

Invalid transitions return:

```text
409 Conflict
```

with an appropriate business error code.

---

# 16. Domain Behaviour

Execution exposes the following business methods.

```text
start()

complete()

fail(reason)

cancel(reason)
```

Execution state shall never be modified through direct property assignment.

---

# 17. Domain Events

Execution state transitions generate events.

Examples

* ExecutionStarted
* ExecutionCompleted
* ExecutionFailed
* ExecutionCancelled

These events support:

* Audit
* Dashboard
* Notifications
* Future LIMS integration

---

# 18. Architectural Rules

1. Execution records actual laboratory activity.
2. Assignment records planned activity.
3. Execution never modifies planning decisions.
4. Planned timestamps and actual timestamps are independent.
5. Execution state transitions are auditable.
6. Execution is append-only from a historical perspective.

---

# 19. Future Extension

Future versions may support:

* Pause / Resume
* Retry
* Multiple execution attempts
* Instrument event synchronization
* Automatic execution updates from instrument interfaces

These features extend the Execution lifecycle without affecting the Planning Domain.
