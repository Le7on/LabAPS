# docs/04_ADR/ADR-002-Plan-Version-Instead-of-Planning-Session.md

# ADR-002 — Plan + Plan Version Instead of Planning Session

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

During the architecture design of Lab APS, several alternatives were considered for representing planning iterations.

The laboratory planning process frequently involves recalculating schedules before publication.

Typical situations include:

* PI changes production demand.
* Equipment becomes unavailable.
* Staff leave changes.
* Laboratory manager adjusts planning manually.

The architecture must preserve historical planning results while supporting repeated schedule generation.

Three alternatives were evaluated.

Option A

```text
Plan
```

Option B

```text
Planning Session

↓

Plan
```

Option C

```text
Plan

↓

Plan Version
```

---

# Decision

Lab APS adopts the following planning model.

```text
Plan
    │
    └── Plan Version
```

Plan represents the business identity.

Plan Version represents one complete planning result.

Each execution of the Scheduling Engine generates a new Plan Version.

Published execution is always based on one specific Plan Version.

---

# Rationale

## Business Language

Laboratory managers naturally refer to:

* Week 32 Production Plan
* Week 33 Production Plan

They rarely use concepts such as "Planning Session".

The architecture should use the same language as laboratory users.

---

## Stable Business Identity

A Plan remains stable throughout its lifetime.

Only its planning result changes.

Separating identity from planning output makes the model easier to understand.

---

## Version History

Every scheduling attempt becomes an independent Plan Version.

Example

```text
Week 32 Plan

├── Version 1
├── Version 2
└── Version 3 (Published)
```

Historical versions remain available for comparison and audit.

---

## Reproducibility

Each Plan Version contains its own:

* Planning Context
* Demand Snapshot
* Workflow Instances
* Assignments
* Material Forecast
* KPI

Therefore every version can be reproduced independently.

---

## Future Scenario Support

Future versions may introduce:

* Simulation
* Emergency
* Alternative Planning

without introducing another business object.

This is achieved through the Version Type.

Example

| Version | Type       |
| ------- | ---------- |
| V1      | Working    |
| V2      | Simulation |
| V3      | Published  |

---

# Alternatives Considered

## Option A — Plan Only

```text
Plan
```

Rejected.

Every recalculation would overwrite the previous schedule.

Historical traceability would be lost.

Audit requirements could not be satisfied.

---

## Option B — Planning Session

```text
Planning Session

↓

Plan
```

Rejected for Version 1.0.

Planning Session introduces another business concept that laboratory users do not recognize.

Although common in enterprise APS products, it increases conceptual complexity without providing sufficient value for the current scope.

The same business requirements are satisfied by Plan + Plan Version.

Planning Session may be reconsidered if future requirements include:

* Multiple concurrent planning teams
* Cross-site planning
* Independent planning workspaces

---

## Option C — ParentPlan Relationship

```text
Plan

↓

ParentPlan
```

Rejected.

Using recursive parent relationships to represent versions complicates:

* Queries
* Reporting
* Version management

A dedicated Plan Version entity provides a clearer model.

---

# Consequences

Positive

* Stable business identity.
* Clear version history.
* Simpler API design.
* Simpler reporting.
* Better auditability.
* Easier comparison between versions.

Negative

* Plan Version becomes a large aggregate.
* More storage is required because each version stores planning snapshots.

The additional storage cost is considered acceptable because planning data is generated weekly rather than continuously.

---

# Implementation Notes

The following implementation rules are mandatory.

1. A Plan owns one or more Plan Versions.

2. Every scheduling execution creates a new Plan Version.

3. Published Plan Versions are immutable.

4. Only one Plan Version may have Published status.

5. All execution records reference the Published Plan Version.

6. Planning Context belongs to the Plan Version.

7. Demand belongs to the Plan Version.

8. Assignments belong to the Plan Version.

---

# Related Documents

* SAD Chapter 4 — Plan Aggregate
* SAD Chapter 8 — Plan Lifecycle
* SAD Chapter 9 — Plan Version Architecture
* SAD Chapter 10 — Persistence Architecture
* ADR-001 — Plan as the Aggregate Root
