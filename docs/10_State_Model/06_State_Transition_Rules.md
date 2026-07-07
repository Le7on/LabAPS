# docs/10_State_Model/04_State_Transition_Rules.md

# State Model

## Chapter 4 - State Transition Rules

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the common transition rules shared by every State Machine in Lab APS.

Rather than repeating transition behaviour for each business object, this document establishes one consistent transition policy.

All business state machines inherit these rules.

---

# 2. Design Principles

Every state transition shall satisfy the following principles.

### Principle 1

A transition is a business decision.

It is never a database update.

---

### Principle 2

Every transition has exactly one trigger.

Transitions never occur automatically without an explicit business event.

---

### Principle 3

Every transition is validated.

Invalid transitions shall fail before persistence.

---

### Principle 4

Every successful transition is auditable.

---

### Principle 5

Every successful transition produces a Domain Event.

---

# 3. State Transition Pipeline

Every state transition follows the same lifecycle.

```text id="st001"
Business Action

↓

Permission Check

↓

State Validation

↓

Business Validation

↓

Transition

↓

Domain Event

↓

Persistence

↓

Audit Log
```

Every step is mandatory.

---

# 4. Trigger

A transition always begins with one business action.

Examples

```text id="st002"
Generate Schedule

Approve

Publish

Start

Complete

Fail

Archive
```

Actions are initiated by users or approved system processes.

---

# 5. Permission Validation

The Application Layer verifies that the current user may perform the requested action.

Examples

Planner

- Publish

Operator

- Start Assignment

Administrator

- Archive Plan

Permission validation occurs before Domain validation.

---

# 6. State Validation

The Domain verifies that the current state allows the requested action.

Example

```text id="st003"
Current

Working

Action

Publish

Result

Rejected
```

Only valid transitions may continue.

---

# 7. Business Validation

Additional business rules are evaluated.

Examples

Publish requires:

- Approved state
- No blocking validation errors

Start Execution requires:

- Published Plan Version
- Assignment in Ready state

Business validation is independent of state validation.

---

# 8. Transition Execution

If validation succeeds:

- Current State changes.
- Transition timestamp is recorded.
- Transition user is recorded.

The transition occurs inside one transaction.

---

# 9. Domain Event

Every successful transition generates exactly one Domain Event.

Examples

```text id="st004"
PlanVersionPublished

AssignmentStarted

ExecutionCompleted

EquipmentDisabled
```

Domain Events are immutable.

---

# 10. Persistence

The Repository persists the updated Aggregate.

No additional business logic is executed during persistence.

Repositories shall never initiate state transitions.

---

# 11. Audit Logging

Every transition records:

- Aggregate ID
- Previous State
- New State
- Trigger
- User
- Timestamp

Audit records are append-only.

---

# 12. Failure Handling

If any validation fails:

- State remains unchanged.
- No Domain Event is generated.
- No persistence occurs.
- No audit record is written.

The transition is atomic.

---

# 13. Transition Rules

Every transition shall satisfy:

1. One trigger.
2. One transaction.
3. One resulting state.
4. One Domain Event.
5. One Audit Record.

No transition may partially complete.

---

# 14. Architectural Rules

1. Only Domain Objects may change their own state.

2. Repositories never modify state.

3. UI never modifies state.

4. APIs request actions rather than states.

5. State values shall never be assigned directly.

Example

Forbidden

```python id="st005"
assignment.status = AssignmentStatus.RUNNING
```

Required

```python id="st006"
assignment.start()
```

---

# 15. Relationship to Other Documents

This document defines the common transition contract.

Individual state machines define:

- valid states
- valid transitions
- business-specific rules

The transition mechanism defined here applies to:

- Plan
- Plan Version
- Assignment
- Execution
- Equipment
- Staff

without modification.
