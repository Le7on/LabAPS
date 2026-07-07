# docs/10_State_Model/07_Equipment_State.md

# State Model

## Chapter 7 - Equipment State Machine

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the business state model for laboratory equipment.

Unlike planning objects, Equipment is a long-lived resource.

Equipment participates in scheduling only when it is operationally available.

This document separates equipment configuration from operational availability.

---

# 2. Design Philosophy

Equipment has two independent state dimensions.

```text id="eqs001"
Configuration State

+

Operational State
```

Configuration answers:

> Should this equipment exist in the laboratory?

Operational State answers:

> Can this equipment participate in scheduling now?

These two concerns must remain independent.

---

# 3. Configuration State

Configuration State changes rarely.

Lifecycle

```text id="eqs002"
Enabled

↓

Disabled

↓

Retired
```

---

## Enabled

The equipment is part of the laboratory.

It may participate in future planning if operationally available.

---

## Disabled

The equipment is temporarily unavailable as a laboratory resource.

Reasons may include:

- Administrative decision
- Temporary removal
- Validation activities

Disabled equipment is excluded from new planning.

Historical Plans remain unchanged.

---

## Retired

The equipment has permanently left service.

Retired equipment:

- cannot be enabled again
- cannot participate in future planning

Historical planning remains available.

---

# 4. Operational State

Operational State reflects the current scheduling availability.

Version 1.0 supports the following states.

```text id="eqs003"
Available

↓

Unavailable
```

Operational availability is determined by business conditions rather than manual state changes.

---

## Available

Equipment satisfies all scheduling requirements.

Examples

- Enabled
- No maintenance
- FV qualification valid

Available equipment may be allocated by the Scheduling Engine.

---

## Unavailable

Equipment cannot participate in scheduling.

Typical reasons include:

- Planned Maintenance
- Unexpected Failure
- FV Qualification Expired

The reason shall be recorded separately.

Unavailable equipment remains visible in the system.

---

# 5. Availability Evaluation

Operational State is derived from laboratory facts.

Example

```text id="eqs004"
Enabled

+

No Maintenance

+

FV Valid

↓

Available
```

Example

```text id="eqs005"
Enabled

+

Maintenance

↓

Unavailable
```

The application shall derive availability.

It shall not rely on manual updates whenever possible.

---

# 6. State Transitions

## Configuration State

```text id="eqs006"
Enabled

↓

Disable

↓

Disabled

↓

Retire

↓

Retired
```

Retirement is irreversible.

---

## Operational State

Operational availability changes automatically according to:

- Maintenance Schedule
- Qualification Status
- Equipment Health

Operational State is recalculated whenever planning begins.

---

# 7. Business Rules

EQ-001

Only Enabled equipment may become Available.

---

EQ-002

Retired equipment is permanently excluded from planning.

---

EQ-003

Unavailable equipment shall not receive new Assignments.

---

EQ-004

Historical Assignments referencing unavailable or retired equipment remain valid.

---

EQ-005

Operational State is derived.

Configuration State is managed.

---

# 8. Scheduling Behaviour

The Scheduling Engine evaluates Operational State only.

Configuration State is resolved before scheduling begins.

Planning Context captures the effective availability snapshot.

The Solver never evaluates maintenance schedules directly.

---

# 9. UI Behaviour

Configuration View

Actions

- Enable
- Disable
- Retire

Planning View

Displays

- Available
- Unavailable

The planner does not edit Operational State manually.

---

# 10. API Behaviour

Configuration Commands

```http id="eqs007"
POST /equipment/{id}:disable

POST /equipment/{id}:retire

POST /equipment/{id}:enable
```

No API exists for:

```http id="eqs008"
POST /equipment/{id}:available
```

Availability is calculated automatically.

---

# 11. Domain Behaviour

Equipment exposes business methods.

```text id="eqs009"
enable()

disable()

retire()
```

Operational availability is exposed as a derived property.

```text id="eqs010"
is_available()
```

The availability calculation shall remain inside the Domain.

---

# 12. Related Documents

- State Model — State Transition Rules
- Planning Context
- Constraint Framework
- Planning Problem
- Scheduling Model

The Scheduling Engine consumes only the calculated availability, never the underlying maintenance or qualification logic.
