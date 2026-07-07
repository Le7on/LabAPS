# docs/03_SAD/05_Scheduling_Architecture.md

# Software Architecture Design

## Chapter 5 - Scheduling Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the Scheduling Architecture of Lab APS.

Scheduling is responsible for transforming planning data into an optimized execution schedule.

Scheduling is an Optimization Service inside the Planning Domain.

Scheduling does not own business data.

Scheduling does not define laboratory workflows.

Scheduling performs optimization only.

---

# 2. Scheduling Responsibilities

Scheduling is responsible for:

- Building optimization variables
- Building optimization constraints
- Defining optimization objectives
- Executing the Solver
- Converting solver results into Assignments

Scheduling is NOT responsible for:

- Workflow generation
- Demand management
- Equipment management
- Staff management
- Plan lifecycle

---

# 3. Scheduling Pipeline

The Scheduling Engine executes the following pipeline.

```text
Plan
 │
 ▼
Operation Collection
 │
 ▼
Scheduling Model Builder
 │
 ▼
Constraint Builder
 │
 ▼
Objective Builder
 │
 ▼
Solver Adapter
 │
 ▼
Solver Result
 │
 ▼
Assignment Builder
 │
 ▼
Plan
```

The Plan remains the owner of all generated Assignments.

---

# 4. Scheduling Input

Scheduling receives exactly one Plan.

The Plan provides:

- Operations
- Planning Context
- Resource Snapshots

Scheduling never queries the database directly.

---

# 5. Scheduling Model

Before optimization, Planning data is converted into an internal Scheduling Model.

The Scheduling Model contains only optimization information.

Example

```text
Operation

Duration

Required Capability

Required Skill

Dependencies

Allowed Shifts
```

Business information is removed.

The Scheduling Model exists only in memory.

---

# 6. Internal Scheduling Graph

The Scheduling Model internally constructs a Directed Acyclic Graph (DAG).

Each node represents one Operation.

Each edge represents one dependency.

Example

```text
SMDP
  │
  ├────────► SAP-1
  │
  ├────────► SAP-2
  │
  └────────► SAP-3
```

The graph is an implementation detail.

It is never persisted.

---

# 7. Variable Builder

Variable Builder creates optimization variables.

Examples include:

Assignment Variable

Represents whether an Operation is assigned to:

- Equipment
- Staff
- Shift

Start Variable

Represents the start time of an Operation.

End Variable

Represents the finish time of an Operation.

Variable Builder contains no business rules.

---

# 8. Constraint Builder

Constraint Builder converts business constraints into optimization constraints.

Constraint groups include:

## Resource Constraints

- Equipment Capacity
- Staff Capacity

---

## Capability Constraints

- Required Equipment Capability
- Required Staff Skill

---

## Workflow Constraints

- Operation Dependencies
- Intermediate Resource Availability

---

## Calendar Constraints

- Shift Availability
- Holidays
- Leave
- Maintenance

---

## Qualification Constraints

- FV Qualification

Constraint Builder receives only the Scheduling Model.

It never queries Master Data.

---

# 9. Objective Builder

Objective Builder defines optimization goals.

Version 1.0 supports weighted objectives.

Suggested priorities:

1. Maximize demand completion.

2. Minimize scheduling conflicts.

3. Maximize equipment utilization.

4. Balance staff workload.

Objective weights are configurable through Solver Profiles.

---

# 10. Solver Adapter

The Solver Adapter encapsulates Google OR-Tools.

Responsibilities:

- Create CP-SAT Model
- Invoke Solver
- Capture Solver Status
- Return Solution

No business logic belongs in the Solver Adapter.

The Solver Adapter may be replaced without changing the Planning Domain.

---

# 11. Assignment Builder

After optimization completes, Assignment Builder converts solver output into business objects.

Each Assignment contains:

- Operation
- Equipment
- Staff
- Shift
- Planned Start Time
- Planned End Time

Assignments are attached to the originating Plan.

---

# 12. Scheduling Result

The Scheduling Engine returns:

- Assignments
- Solver Status
- Solver Runtime
- Optimization Score
- Warning Messages

The Scheduling Engine does not update the database.

Persistence is handled by the Application Layer.

---

# 13. Error Handling

Scheduling errors are categorized as follows.

Validation Errors

Examples:

- Missing Workflow Template
- Missing Capability
- Missing Skill

Validation errors prevent scheduling.

Optimization Errors

Examples:

- No feasible schedule
- Solver timeout

Optimization errors return partial diagnostic information.

System Errors

Examples:

- Unexpected exception
- Infrastructure failure

System errors are logged and propagated to the Application Layer.

---

# 14. Extension Points

The Scheduling Architecture is designed to support future extensions.

Examples include:

- Additional constraint builders
- Alternative optimization objectives
- Multiple solver implementations
- Parallel solving strategies

The Planning Domain remains unchanged when these extensions are added.

---

# 15. Architectural Rules

The following rules are mandatory.

1. Scheduling receives exactly one Plan.

2. Scheduling never queries the database.

3. Scheduling never modifies Master Data.

4. Scheduling never modifies Configuration.

5. Scheduling owns no business entities.

6. Scheduling produces Assignments only.

7. OR-Tools is isolated behind the Solver Adapter.

8. All optimization data exists only in memory.

9. Internal graph structures are implementation details and are never persisted.
