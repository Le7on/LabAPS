# docs/04_ADR/ADR-003-Workflow-Definition-and-Workflow-Instance.md

# ADR-003 — Separate Workflow Definition from Workflow Instance

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

Laboratory workflows evolve over time.

Examples include:

- Process optimization
- Additional validation steps
- New instrument support
- Changed operation duration
- Updated material consumption
- New dependency rules

However, historical production plans must remain reproducible.

This creates a conflict.

If workflow definitions are modified directly, historical Plans would reference changed workflow definitions, making historical schedules impossible to reproduce accurately.

---

# Decision

Lab APS separates workflow definitions from workflow execution.

```text id="adr3-001"
Project
    │
    ▼
Workflow Definition
    │
    ▼
Operation Definition
```

During planning:

```text id="adr3-002"
Workflow Definition

↓

Workflow Instance

↓

Operation Instance
```

Workflow Definition belongs to Laboratory Definition.

Workflow Instance belongs to Plan Version.

---

# Rationale

## Workflow Definition is Knowledge

Workflow Definition represents laboratory process knowledge.

Examples include:

- Process sequence
- Operation definitions
- Dependency rules
- Material BOM
- Intermediate resources

These describe **how** a laboratory project should be executed.

They are reusable.

---

## Workflow Instance is Execution

Workflow Instance represents one generated execution of a workflow.

Example

Demand

```text id="adr3-003"
384 PNG

Quantity = 3
```

Produces

```text id="adr3-004"
PNG-001

PNG-002

PNG-003
```

Each Workflow Instance exists only inside one Plan Version.

---

## Historical Stability

Workflow Definitions may change over time.

Example

```text id="adr3-005"
Workflow Definition V1

↓

Workflow Definition V2
```

Existing Plan Versions continue referencing the Workflow Definition that was active when they were generated.

Historical planning remains reproducible.

---

## Clear Ownership

Workflow Definition belongs to Laboratory Definition.

Workflow Instance belongs to Planning.

The two domains remain independent.

---

# Alternatives Considered

## Option A — Workflow Only

```text id="adr3-006"
Workflow
```

Rejected.

A single object cannot simultaneously represent:

- laboratory knowledge
- generated planning data

Updating the workflow would invalidate historical planning.

---

## Option B — Copy Workflow into Every Plan

Rejected.

Copying complete workflow definitions into every Plan would duplicate configuration data and complicate maintenance.

Only execution instances should belong to planning.

---

## Option C — Dynamic Workflow Lookup

Rejected.

Resolving the latest workflow during execution would make historical Plans non-reproducible.

Published planning must always be deterministic.

---

# Consequences

Positive

- Workflow evolution is supported.
- Historical Plans remain reproducible.
- Workflow Templates remain reusable.
- Planning data remains isolated.
- Workflow Engine has a clear responsibility.

Negative

- Additional entities are introduced.
- Workflow generation becomes an explicit planning step.

These costs are acceptable given the long-term maintainability benefits.

---

# Architectural Rules

1. Workflow Definitions belong to Laboratory Definition.

2. Workflow Instances belong to Plan Version.

3. Workflow Definitions are reusable.

4. Workflow Instances are generated automatically.

5. Users never create Workflow Instances manually.

6. Workflow Definitions shall not contain execution state.

7. Workflow Instances shall not modify Workflow Definitions.

8. Workflow Definition changes never affect existing Plan Versions.

---

# Implementation Notes

Workflow generation follows this sequence.

```text id="adr3-007"
Demand

↓

Project

↓

Workflow Definition

↓

Workflow Generator

↓

Workflow Instance

↓

Operation Instance
```

The Workflow Generator is responsible for transforming reusable process definitions into executable planning objects.

The Scheduling Engine never accesses Workflow Definitions directly.

It operates only on Operation Instances produced by the Workflow Generator.

---

# Related Documents

- SRS Chapter 5 — Business Object Model
- SAD Chapter 3 — Domain Architecture
- SAD Chapter 7 — Conceptual Database Model
- SAD Chapter 10 — Conceptual ERD
- ADR-001 — Plan as the Aggregate Root
- ADR-002 — Plan + Plan Version
