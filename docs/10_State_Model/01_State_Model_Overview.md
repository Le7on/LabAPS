# docs/10_State_Model/01_State_Model_Overview.md

# State Model

## Chapter 1 - State Model Overview

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the business state model used throughout Lab APS.

The objective is to provide one consistent definition of every business object's lifecycle.

State definitions are shared by:

* Domain Model
* REST API
* User Interface
* Repository
* Reporting
* Testing

Every business state shall be defined only once.

---

# 2. Design Philosophy

Business Objects evolve through well-defined lifecycle states.

A state represents the current business meaning of an object.

It is **not** merely a database value.

Every state transition shall:

* have a business reason
* have a valid trigger
* produce a business result

---

# 3. State Categories

Lab APS contains six major state machines.

```text id="sm001"
Plan

Plan Version

Assignment

Execution

Equipment

Staff
```

Each business object owns exactly one lifecycle.

---

# 4. State Machine Principles

The following principles apply to every state machine.

### Principle 1

Every object is always in exactly one state.

---

### Principle 2

Transitions are explicit.

No implicit state changes are allowed.

---

### Principle 3

Only valid transitions are permitted.

Invalid transitions shall produce Business Validation Errors.

---

### Principle 4

State transitions are initiated by business actions.

Examples

* Publish
* Complete
* Archive
* Disable

State changes never occur without a triggering action.

---

### Principle 5

Every state transition is auditable.

The system shall record:

* Previous State
* New State
* Time
* User
* Trigger

---

# 5. Generic State Machine

Every business object follows the same conceptual lifecycle.

```text id="sm002"
Created

↓

Working

↓

Completed

↓

Archived
```

Individual objects specialize this generic lifecycle.

---

# 6. State Ownership

Each state machine belongs to one Aggregate.

| State Machine | Aggregate    |
| ------------- | ------------ |
| Plan          | Plan         |
| Plan Version  | Plan         |
| Assignment    | Plan Version |
| Execution     | Execution    |
| Equipment     | Equipment    |
| Staff         | Staff        |

State transitions shall always occur through the owning Aggregate.

---

# 7. Transition Rules

Every transition defines:

* Current State
* Trigger
* Next State
* Validation
* Side Effects

Example

```text id="sm003"
Current

Reviewed

Trigger

Publish

Next

Published
```

The trigger is a business action rather than a database update.

---

# 8. Business Events

Every successful transition produces a Domain Event.

Examples

```text id="sm004"
PlanPublished

AssignmentStarted

AssignmentCompleted

ExecutionFinished

EquipmentDisabled
```

Events may later be used for:

* Audit
* Notification
* Integration
* Analytics

Version 1.0 records events but does not require asynchronous processing.

---

# 9. State Validation

State validation occurs inside the Domain Layer.

Examples

Valid

```text id="sm005"
Reviewed

↓

Published
```

Invalid

```text id="sm006"
Draft

↓

Completed
```

Invalid transitions shall raise Business Exceptions.

Repositories shall never enforce business state transitions.

---

# 10. UI Behaviour

The User Interface reflects the current state.

Examples

Draft

* Generate Schedule enabled
* Publish disabled

Published

* Generate Schedule disabled
* Publish disabled
* Execution available

The UI never determines state.

It only reflects the Domain state.

---

# 11. API Behaviour

The REST API follows the state model.

Examples

Attempting to publish an invalid Plan Version returns:

```text id="sm007"
409 Conflict
```

Attempting to edit a Published Plan Version returns:

```text id="sm008"
409 Conflict
```

The API does not implement state rules.

The Domain Layer does.

---

# 12. Persistence Behaviour

The database stores the current state only.

State history is maintained through:

* Audit Log
* Activity Log
* Domain Events

Historical transitions are not inferred from database updates.

---

# 13. Testing Requirements

Every state machine shall have dedicated tests covering:

* Valid transitions
* Invalid transitions
* Boundary conditions
* Business exceptions
* Side effects

State transition coverage is mandatory.

---

# 14. Future Extension

Future business objects shall define their lifecycle by creating a dedicated state machine.

Existing state machines shall not be overloaded to represent unrelated concepts.

---

# 15. Next Documents

The following documents define each state machine in detail.

```text id="sm009"
02_Plan_State.md

03_PlanVersion_State.md

04_Assignment_State.md

05_Execution_State.md

06_Equipment_State.md

07_Staff_State.md
```

These documents inherit the principles established in this overview.
