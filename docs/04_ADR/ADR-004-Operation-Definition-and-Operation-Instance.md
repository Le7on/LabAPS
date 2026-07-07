# docs/04_ADR/ADR-004-Operation-Definition-and-Operation-Instance.md

# ADR-004 — Separate Operation Definition from Operation Instance

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

Each laboratory workflow consists of one or more logical operations.

Examples include:

- FV
- SMDP
- SAP
- CP
- SP

These operations are reusable process definitions.

During planning, however, the Scheduler must allocate concrete executable work items.

The following design alternatives were considered:

Option A

```text
Operation
```

Option B

```text
Operation Definition

↓

Operation Instance
```

The architecture must support:

- Workflow reuse
- Historical traceability
- Scheduling
- Future workflow evolution

---

# Decision

Lab APS separates operation definitions from execution instances.

```text
Operation Definition
        │
        ▼
Operation Instance
```

Operation Definition belongs to Workflow Definition.

Operation Instance belongs to Workflow Instance.

Only Operation Instances participate in scheduling.

---

# Rationale

## Separation of Definition and Execution

Operation Definition describes laboratory knowledge.

Examples

- Operation Name
- Logical Sequence
- Default Duration
- Required Capability
- Required Skill
- Material BOM

Operation Definition contains no execution state.

---

Operation Instance represents one executable activity.

Examples

```text
PNG-001

└── SMDP
```

```text
PNG-001

└── SAP
```

Each Operation Instance owns execution information.

---

## Scheduling

Scheduling requires executable work.

The Solver allocates:

- Staff
- Equipment
- Shift

These allocations belong to Operation Instances.

They do not belong to Operation Definitions.

---

## Historical Traceability

Workflow Definitions may evolve.

Operation Definitions may evolve as well.

Historical Plan Versions continue referencing the Operation Definition version that was active during planning.

Historical execution remains reproducible.

---

# Alternatives Considered

## Option A — Operation Only

```text
Operation
```

Rejected.

A single object would need to represent both:

- process definition
- execution state

This mixes two different responsibilities.

---

## Option B — Assignment Directly References Operation Definition

Rejected.

Assignments represent planned execution.

Execution always occurs on one generated Operation Instance.

Referencing definitions directly would make it impossible to distinguish between different executions of the same workflow.

---

## Option C — Generate Assignment Directly from Workflow

Rejected.

Assignments require the smallest executable unit.

Workflow contains multiple operations and therefore cannot be scheduled directly.

---

# Consequences

Positive

- Clear separation between definition and execution.
- Easier workflow evolution.
- Simpler scheduling model.
- Better historical traceability.
- Cleaner domain boundaries.

Negative

- One additional entity is introduced.

This additional complexity is justified because it aligns with the business model and simplifies scheduling.

---

# Architectural Rules

1. Operation Definitions belong to Workflow Definitions.

2. Operation Instances belong to Workflow Instances.

3. Users configure Operation Definitions.

4. Users never create Operation Instances manually.

5. Operation Instances are generated automatically during planning.

6. Assignments always reference Operation Instances.

7. Execution status belongs to Operation Instances.

8. Operation Definitions remain reusable and stateless.

---

# Scheduling Implications

The Scheduling Engine receives only Operation Instances.

Operation Definitions are consumed only during Workflow generation.

The scheduling pipeline becomes:

```text
Workflow Definition

↓

Workflow Generator

↓

Workflow Instance

↓

Operation Instance

↓

Scheduling Model

↓

Solver

↓

Assignment
```

This pipeline clearly separates:

- Process Definition
- Planning
- Optimization
- Execution

---

# Related Documents

- ADR-003 — Workflow Definition and Workflow Instance
- SAD Chapter 5 — Scheduling Architecture
- SAD Chapter 7 — Conceptual Database Model
- SAD Chapter 11 — Physical Database Design
- SAD Chapter 14 — Solver Model
