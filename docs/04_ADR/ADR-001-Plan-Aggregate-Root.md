# docs/04_ADR/ADR-001-Plan-Aggregate-Root.md

# ADR-001 — Plan as the Aggregate Root

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

Lab APS is a laboratory planning platform rather than a laboratory execution system.

During architecture design, several candidate Aggregate Roots were considered:

* Demand
* Workflow Instance
* Operation Instance
* Assignment
* Planning Session
* Plan

Each candidate was evaluated against the following requirements:

* Represent one complete planning cycle.
* Support multiple schedule generations.
* Support historical traceability.
* Support future scenario planning.
* Maintain transactional consistency.
* Remain understandable to laboratory users.

---

# Decision

**Plan** is selected as the Aggregate Root of the Planning Domain.

All planning data shall belong to exactly one Plan.

A Plan owns:

* Plan Versions
* Planning Context
* Demand
* Workflow Instances
* Operation Instances
* Assignments
* Material Forecast
* KPI

No planning object may exist independently of a Plan.

---

# Rationale

## Business Identity

Laboratory managers naturally think in terms of:

* Week 32 Production Plan
* Week 33 Production Plan

They do not think in terms of individual Workflow Instances.

Therefore the Aggregate Root should match the business identity.

---

## Transaction Boundary

Publishing a schedule requires consistency across:

* Demand
* Assignments
* Material Forecast
* KPI

Managing these through separate aggregates would require distributed coordination.

Using Plan as the Aggregate Root provides a single transactional boundary.

---

## Traceability

Every planning artifact can be traced back to:

* one Plan
* one Planning Horizon
* one Plan Version

This greatly simplifies auditing and reporting.

---

## Future Expansion

Future features such as:

* Scenario Planning
* Multi-week Planning
* AI Recommendations

can be introduced without changing the Aggregate Root.

---

# Alternatives Considered

## Option A — Demand as Aggregate Root

Rejected.

Demand defines **what** should be completed.

It does not own scheduling results.

---

## Option B — Workflow Instance as Aggregate Root

Rejected.

Workflow Instances are generated objects.

They are subordinate to planning.

A production plan normally contains many Workflow Instances.

---

## Option C — Operation Instance as Aggregate Root

Rejected.

Operation Instances are implementation details of workflow execution.

Managing them independently would significantly increase complexity.

---

## Option D — Assignment as Aggregate Root

Rejected.

Assignments represent scheduling results only.

They do not own planning context or demand.

---

## Option E — Planning Session

Rejected for Version 1.0.

Planning Session introduces an additional business concept that is not required by the current laboratory workflow.

The existing Plan + Plan Version model satisfies current requirements while remaining extensible.

---

# Consequences

Positive:

* Clear ownership of planning data.
* Simple repository structure.
* Straightforward API design.
* Strong transactional consistency.
* Easy version management.

Negative:

* Plan Aggregate becomes relatively large.
* Loading strategy must be optimized to avoid unnecessary data retrieval.

These concerns are addressed through:

* lazy loading
* DTO projections
* dedicated reporting queries

rather than changing the aggregate boundary.

---

# Related Documents

* SRS Chapter 3 — Business Process
* SAD Chapter 4 — Plan Aggregate
* SAD Chapter 8 — Plan Lifecycle
* SAD Chapter 9 — Plan Version Architecture
* SAD Chapter 10 — Persistence Architecture

---

# Implementation Notes

The implementation shall follow these rules:

1. Only `PlanRepository` persists planning data.
2. Child entities are created through the Plan Aggregate.
3. Published Plan Versions are immutable.
4. Every scheduling operation begins with loading a Plan and creating a new Plan Version.
5. Future features shall extend the Planning Domain without changing the Aggregate Root.
