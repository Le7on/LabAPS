# docs/10_State_Model/08_Staff_State.md

# State Model

## Chapter 8 - Staff State Machine

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the business state model for laboratory staff.

Staff is a long-lived laboratory resource.

Like Equipment, Staff participates in planning only when operationally available.

This document separates personnel management from scheduling availability.

---

# 2. Design Philosophy

Staff has two independent state dimensions.

```text
Configuration State

+

Availability State
```

Configuration State answers:

> Should this person be considered part of the laboratory?

Availability State answers:

> Can this person participate in the current planning cycle?

Planning uses Availability State only.

---

# 3. Configuration State

Configuration State changes infrequently.

Lifecycle

```text
Active

↓

Disabled

↓

Inactive
```

---

## Active

The staff member belongs to the laboratory.

The person may participate in planning if available.

---

## Disabled

The staff member is temporarily excluded from planning.

Typical reasons

- Temporary suspension
- Training
- Administrative decision

Historical planning remains unchanged.

---

## Inactive

The staff member has permanently left the laboratory.

Inactive staff cannot participate in future planning.

Historical planning remains available.

---

# 4. Availability State

Availability State is derived automatically.

Version 1.0 supports:

```text
Available

↓

Unavailable
```

Availability is calculated from planning facts.

Users do not edit Availability directly.

---

## Available

The staff member satisfies all scheduling conditions.

Examples

- Active
- Working Day
- Not on Leave

Available staff may receive Assignments.

---

## Unavailable

The staff member cannot participate in scheduling.

Typical causes include:

- Leave
- Holiday
- Outside Working Calendar

The reason shall be traceable.

---

# 5. Availability Evaluation

Availability is derived from business facts.

Example

```text
Active

+

Working Day

+

No Leave

↓

Available
```

Example

```text
Active

+

Annual Leave

↓

Unavailable
```

The Scheduling Engine consumes only the resulting Availability.

---

# 6. State Transitions

## Configuration State

```text
Active

↓

Disable

↓

Disabled

↓

Deactivate

↓

Inactive
```

Inactive is a terminal state.

---

## Availability State

Availability is recalculated whenever a Planning Context is generated.

Typical inputs

- Staff Leave
- Calendar
- Working Hours

Availability is not persisted as a manually maintained business value.

---

# 7. Business Rules

ST-001

Only Active staff may become Available.

---

ST-002

Inactive staff shall never participate in planning.

---

ST-003

Unavailable staff shall not receive new Assignments.

---

ST-004

Historical Assignments remain valid even if the staff member later becomes Inactive.

---

ST-005

Availability is derived from planning facts rather than manually maintained.

---

# 8. Scheduling Behaviour

The Scheduling Engine evaluates only Availability.

Configuration State is resolved before scheduling begins.

Planning Context stores the effective availability snapshot.

The Solver does not evaluate leave calendars directly.

---

# 9. UI Behaviour

Configuration View

Actions

- Activate
- Disable
- Deactivate

Planning View

Displays

- Available
- Unavailable

Operational availability is read-only.

---

# 10. API Behaviour

Configuration Commands

```http
POST /staff/{id}:disable

POST /staff/{id}:activate

POST /staff/{id}:deactivate
```

No API exists for:

```http
POST /staff/{id}:available
```

Availability is calculated automatically.

---

# 11. Domain Behaviour

Staff exposes configuration behaviour.

Examples

```text
activate()

disable()

deactivate()
```

Availability is exposed as a derived business property.

```text
is_available(planning_context)
```

The Domain determines availability.

Neither the UI nor the Solver computes it.

---

# 12. Relationship to Planning Context

During planning, Staff Availability is captured as part of the Planning Context.

The Planning Context contains the effective scheduling snapshot.

Future changes to leave or calendars do not affect existing Plan Versions.

---

# 13. Resource Model Consistency

Equipment and Staff follow the same scheduling model.

| Concept              | Equipment | Staff |
| -------------------- | --------- | ----- |
| Configuration State  | Yes       | Yes   |
| Availability State   | Yes       | Yes   |
| Availability Derived | Yes       | Yes   |
| Snapshot Stored      | Yes       | Yes   |

This provides a unified Resource Model for the Planning Engine.

---

# 14. Related Documents

- State Model — State Transition Rules
- State Model — Equipment State
- Planning Context
- Constraint Framework
- Planning Problem

The Scheduling Engine treats Staff and Equipment uniformly through the Resource Availability model.
