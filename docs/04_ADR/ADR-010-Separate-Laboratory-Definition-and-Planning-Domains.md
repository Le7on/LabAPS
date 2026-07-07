# docs/04_ADR/ADR-010-Separate-Laboratory-Definition-and-Planning-Domains.md

# ADR-010 — Separate Laboratory Definition and Planning Domains

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

During the architecture design of Lab APS, an important question emerged:

Should laboratory configuration and production planning belong to the same business domain?

Initially, all entities were considered part of one large planning module.

```text
Planning

├── Staff
├── Equipment
├── Workflow Definition
├── Plan
├── Assignment
└── Execution
```

Although simple at first glance, this approach mixes two fundamentally different responsibilities.

Laboratory configuration changes slowly.

Planning changes every planning cycle.

These two concepts evolve at different rates.

---

# Decision

Lab APS separates the system into two independent business domains.

```text
Laboratory Definition
        │
        ▼
Planning
```

Laboratory Definition defines **what the laboratory is**.

Planning defines **how the laboratory will be used during a planning horizon**.

Planning consumes information from Laboratory Definition but never owns it.

---

# Laboratory Definition

Laboratory Definition contains long-lived business knowledge.

Examples include:

- Staff
- Equipment
- Capability
- Skill
- Project
- Workflow Definition
- Operation Definition
- Material Definition
- Shift Definition

Characteristics

- Changes infrequently.
- Shared by every Plan.
- Managed by laboratory engineers.
- Represents configuration rather than execution.

Laboratory Definition contains no scheduling results.

---

# Planning

Planning contains short-lived operational information.

Examples include:

- Plan
- PlanVersion
- Planning Context
- Demand
- Workflow Instance
- Operation Instance
- Assignment
- Material Forecast
- KPI

Characteristics

- Generated repeatedly.
- Versioned.
- Time-dependent.
- Represents one planning cycle.

Planning never modifies Laboratory Definition.

---

# Rationale

## Different Business Lifecycles

Laboratory Definition evolves over months.

Planning evolves daily or weekly.

Combining them into one domain would introduce unnecessary coupling.

---

## Different Business Owners

Laboratory Definition is typically maintained by:

- Laboratory Engineer
- System Administrator

Planning is owned by:

- Production Laboratory Manager

Separating the domains reflects actual business responsibilities.

---

## Different Persistence Behaviour

Laboratory Definition is updated.

Planning is versioned.

Historical planning records must remain immutable.

The persistence requirements are therefore different.

---

## Independent Evolution

Examples

Laboratory Definition changes

- Add a new instrument
- Update Workflow Definition
- Add a new Capability

Planning remains unaffected until a new PlanVersion is created.

Likewise,

planning recalculation does not modify laboratory configuration.

---

# Alternatives Considered

## Option A — Single Planning Domain

Rejected.

Configuration and operational planning become tightly coupled.

Historical planning becomes harder to reproduce.

Module responsibilities become unclear.

---

## Option B — Laboratory Definition + Planning

Accepted.

Stable laboratory knowledge is separated from time-dependent planning.

Responsibilities remain clear.

---

# Consequences

Positive

- Clear ownership.
- Independent evolution.
- Better maintainability.
- Easier testing.
- Simpler permissions.
- Cleaner module boundaries.

Negative

- Additional mapping step during planning.

This mapping already exists through the Planning Context and Scheduling Model, so no additional architectural complexity is introduced.

---

# Interaction Rules

The following interactions are permitted.

```text
Laboratory Definition

↓

Planning Context Builder

↓

PlanVersion
```

The following interactions are prohibited.

```text
PlanVersion

↓

Update Staff

PlanVersion

↓

Update Equipment

Assignment

↓

Modify Workflow Definition
```

Planning consumes laboratory definitions.

Planning never changes them.

---

# Architectural Rules

1. Laboratory Definition is the authoritative source of laboratory configuration.

2. Planning owns all operational planning data.

3. Planning Context captures a scheduling snapshot derived from Laboratory Definition.

4. Laboratory Definition shall never reference Plans.

5. Planning shall never persist changes to Laboratory Definition.

6. Communication between domains shall occur through Application Use Cases.

7. Domain repositories remain private to their owning domain.

---

# Impact on Implementation

This decision results in the following package organization.

```text
domain/

    laboratory/

    planning/

    execution/
```

Repository organization.

```text
LaboratoryRepository

PlanningRepository

ExecutionRepository
```

Application layer.

```text
CreatePlanUseCase

↓

Load Laboratory Definition

↓

Build Planning Context

↓

Generate PlanVersion
```

Planning does not access configuration tables directly during scheduling.

Instead, the Planning Context becomes the immutable planning baseline.

---

# Related Documents

- ADR-001 — Plan as the Aggregate Root
- ADR-002 — Plan + Plan Version
- ADR-003 — Workflow Definition and Workflow Instance
- ADR-008 — Planning Context Uses Snapshots
- SAD Chapter 3 — Domain Architecture
- SAD Chapter 9 — Persistence Architecture

---

# Long-Term Impact

This decision establishes the strategic domain boundary of Lab APS.

Future capabilities shall be added to one of these domains rather than introducing unnecessary new domains.

Examples

Laboratory Definition

- New instrument types
- Workflow Definition versions
- Additional capability types

Planning

- Scenario Planning
- Dynamic Rescheduling
- Multi-week Planning
- AI-assisted Planning

Maintaining this separation ensures that laboratory configuration and production planning can evolve independently while preserving a stable and maintainable architecture.
