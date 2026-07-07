# docs/04_ADR/ADR-007-Separate-Constraint-Model-and-Objective-Model.md

# ADR-007 — Separate Constraint Model from Objective Model

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

Scheduling consists of two fundamentally different concepts:

- Feasibility
- Optimization

A schedule must first satisfy mandatory business rules.

Only after a feasible schedule exists should the optimizer attempt to improve schedule quality.

Many scheduling implementations mix these concepts together.

For example:

- Equipment capacity
- Staff availability
- Workload balancing
- Equipment utilization

are all implemented as "constraints".

This makes the optimization model increasingly difficult to understand.

---

# Decision

Lab APS separates the optimization model into two independent parts.

```text
Scheduling Model
        │
        ├── Constraint Model
        │
        └── Objective Model
                │
                ▼
          Solver Adapter
```

Constraint Model defines **what is allowed**.

Objective Model defines **what is preferred**.

---

# Rationale

## Different Business Meaning

Constraint answers:

> Can this schedule exist?

Objective answers:

> Which feasible schedule is better?

These questions belong to different layers of the optimization model.

---

## Different Lifecycle

Constraints usually remain stable.

Examples

- Equipment capacity
- Staff availability
- Workflow dependency
- FV qualification

Objectives change more frequently.

Examples

- Increase throughput
- Reduce overtime
- Balance workload
- Minimize equipment switching

Keeping them independent reduces maintenance cost.

---

## Configurable Optimization

Different laboratories may optimize for different goals.

Examples

Routine Production

- Balance workload
- Maximize equipment utilization

Rush Order

- Maximize completed demand

Validation Week

- Prioritize FV completion

Only the Objective Model changes.

Constraint Model remains unchanged.

---

# Constraint Model

Constraint Model contains mandatory scheduling rules.

Examples include:

## Resource Constraints

- Equipment capacity
- Staff capacity

---

## Requirement Constraints

- Required capability
- Required skill

---

## Workflow Constraints

- Operation dependency
- Intermediate resource dependency

---

## Calendar Constraints

- Shift availability
- Staff leave
- Equipment maintenance

---

## Qualification Constraints

- FV qualification

Violation of any hard constraint produces an infeasible schedule.

---

# Objective Model

Objective Model defines optimization goals.

Version 1.0 supports weighted objectives.

Examples include:

- Maximize completed demand
- Maximize equipment utilization
- Balance staff workload
- Minimize idle equipment
- Minimize unnecessary equipment switching

Objectives may be enabled, disabled or weighted through the Solver Profile.

---

# Solver Adapter

The Solver Adapter receives:

```text
Scheduling Model

Constraint Model

Objective Model
```

The adapter combines these into the OR-Tools CP-SAT model.

Business semantics remain outside the optimization library.

---

# Alternatives Considered

## Option A — Constraints Only

Rejected.

Soft optimization goals become difficult to distinguish from mandatory business rules.

The model loses clarity.

---

## Option B — Constraint Model + Objective Model

Accepted.

The architecture reflects the natural separation between feasibility and optimization.

The resulting model is easier to understand, maintain and extend.

---

# Consequences

Positive

- Clear distinction between hard rules and optimization goals.
- Easier Solver maintenance.
- Easier tuning of optimization strategies.
- Better support for future planning profiles.

Negative

- Additional modeling layer.
- Slightly more implementation effort.

The benefits outweigh the additional complexity.

---

# Architectural Rules

1. Constraint Model defines feasibility only.

2. Objective Model defines optimization preference only.

3. Business rules shall not be implemented as Objective logic.

4. Objective weights shall not modify Constraint definitions.

5. Solver Adapter receives both models independently.

6. Future optimization strategies shall extend Objective Model without changing Constraint Model.

---

# Related Documents

- SAD Chapter 14 — Solver Model
- ADR-005 — Scheduling Model as an Anti-Corruption Layer
- ADR-006 — Constraint Model Instead of Direct Solver Constraints

---

# Future Considerations

Future versions may introduce:

- Optimization Profiles
- Multi-objective optimization
- User-defined objective weighting
- Adaptive optimization strategies

These enhancements shall extend the Objective Model while preserving the existing Constraint Model.
