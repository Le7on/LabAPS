# docs/03_SAD/14_Solver_Model.md

# Software Architecture Design

## Chapter 14 - Solver Model

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the Solver Model used by the Scheduling Engine.

The Solver Model is a normalized optimization model built from the Planning Domain.

It acts as an Anti-Corruption Layer (ACL) between business objects and the optimization engine.

Neither the Domain Model nor the Solver shall depend directly on each other.

---

# 2. Design Goals

The Solver Model shall satisfy the following goals.

* Independent of OR-Tools implementation
* Independent of database schema
* Independent of Flask
* Independent of SQLAlchemy
* Deterministic
* Immutable during solving

The Solver Model exists only in memory.

---

# 3. Solver Pipeline

```text id="sm001"
PlanVersion
        │
        ▼
Planning Validator
        │
        ▼
SchedulingModelBuilder
        │
        ▼
SchedulingModel
        │
        ▼
ConstraintBuilder
        │
        ▼
ObjectiveBuilder
        │
        ▼
SolverAdapter
        │
        ▼
SolverSolution
        │
        ▼
AssignmentBuilder
        │
        ▼
PlanVersion
```

Only the SchedulingModel crosses the boundary into the Solver.

---

# 4. Scheduling Model

The Scheduling Model contains only optimization data.

```text id="sm002"
SchedulingModel

├── ResourceSet
├── OperationSet
├── DependencySet
├── CalendarSet
├── ConstraintSet
└── ObjectiveSet
```

No business entities are exposed.

---

# 5. Resource Set

ResourceSet represents all allocatable resources.

Version 1.0 supports:

```text id="sm003"
Equipment

Staff

Shift
```

Resource attributes include:

Equipment

* ResourceId
* Capability Set
* Available Time Windows

Staff

* ResourceId
* Skill Set
* Available Time Windows

Shift

* ShiftId
* Start Time
* End Time

Future versions may introduce additional resource types without changing the Solver interface.

---

# 6. Operation Set

OperationSet contains every OperationInstance in the current PlanVersion.

Each Operation is transformed into a lightweight scheduling object.

Minimum attributes:

```text id="sm004"
OperationId

Duration

Required Capability Set

Required Skill Set

Allowed Time Window

Priority

Metadata
```

Metadata is optional and ignored by optimization.

---

# 7. Dependency Set

DependencySet represents execution precedence.

Each dependency consists of:

```text id="sm005"
Predecessor Operation

Successor Operation

Relationship Type

Lag
```

Version 1.0 supports:

Finish-to-Start (FS)

Lag defaults to zero.

Future versions may support:

* Start-to-Start
* Finish-to-Finish
* Finish-to-Finish
* Positive / Negative Lag

---

# 8. Calendar Set

CalendarSet represents effective scheduling availability.

Sources include:

* Shift Definition
* Holidays
* Staff Leave
* Equipment Maintenance

The builder converts these into scheduling windows.

Example

```text id="sm006"
HM09

Monday

Shift1

Available

Tuesday

Shift2

Unavailable
```

---

# 9. Constraint Set

ConstraintBuilder transforms business rules into normalized constraints.

Constraint categories:

## Resource Constraints

Examples

* One Equipment executes only one Operation at a time.
* One Staff executes only one Operation at a time.

---

## Capability Constraints

Examples

* Equipment satisfies Capability Requirements.
* Staff satisfies Skill Requirements.

---

## Dependency Constraints

Examples

* SAP starts after SMDP completes.
* SP starts after CP completes.

---

## Qualification Constraints

Examples

Equipment FV qualification must be valid.

---

## Calendar Constraints

Examples

* Staff Leave
* Equipment Maintenance
* Holiday
* Shift Availability

Each constraint is represented as data rather than executable code.

---

# 10. Objective Set

ObjectiveBuilder converts planning strategy into optimization objectives.

Version 1.0 default priorities:

| Priority | Objective                      |
| -------- | ------------------------------ |
| 1        | Maximize completed demand      |
| 2        | Produce a feasible schedule    |
| 3        | Maximize equipment utilization |
| 4        | Balance staff workload         |

Objective weights are provided by the Solver Profile.

The Solver shall not hardcode objective priorities.

---

# 11. SchedulingModelBuilder

SchedulingModelBuilder is responsible for model transformation.

Input

```text id="sm007"
PlanVersion
```

Output

```text id="sm008"
SchedulingModel
```

Responsibilities

* Extract Operations
* Resolve Resource Requirements
* Build Dependency Graph
* Build Calendar Windows
* Normalize data

SchedulingModelBuilder performs no optimization.

---

# 12. SolverAdapter

SolverAdapter encapsulates the optimization engine.

Input

```text id="sm009"
SchedulingModel
```

Output

```text id="sm010"
SchedulingSolution
```

Responsibilities

* Create optimization model
* Execute optimization
* Return normalized solution

SolverAdapter never constructs business objects.

---

# 13. SchedulingSolution

The Solver returns a normalized SchedulingSolution.

Contains:

```text id="sm011"
Assignments

Solver Status

Objective Score

Runtime

Diagnostics
```

The solution remains independent of business entities.

---

# 14. AssignmentBuilder

AssignmentBuilder converts SchedulingSolution into domain objects.

Responsibilities

* Create Assignment
* Populate Planned Start
* Populate Planned End
* Attach Assignment to PlanVersion

Business reconstruction occurs only here.

---

# 15. Validation Boundary

Validation is completed before the Solver starts.

Examples

* Missing Workflow Definition
* Missing Staff Skill Mapping
* Missing Equipment Capability
* Invalid Planning Context

Validation failures prevent SchedulingModel creation.

The Solver assumes valid input.

---

# 16. Performance Principles

The Scheduling Model shall minimize unnecessary data.

Recommended practices:

* Use IDs instead of full entities.
* Convert business objects into immutable records.
* Remove unused metadata.
* Build lookup dictionaries before solving.

This reduces Solver overhead.

---

# 17. Extension Points

Future scheduling features shall be implemented by extending the Scheduling Model.

Examples:

* Intermediate Resource Constraints
* Resource Groups
* Parallel Operations
* Batch Scheduling
* Multi-week Planning

Existing interfaces shall remain unchanged.

---

# 18. Architectural Rules

1. The Solver receives only SchedulingModel.

2. The Solver returns only SchedulingSolution.

3. Business entities never enter the Solver.

4. The SchedulingModel is immutable.

5. The SchedulingSolution is immutable.

6. The Scheduling Engine performs no persistence.

7. OR-Tools is isolated entirely within SolverAdapter.

8. ConstraintBuilder and ObjectiveBuilder produce normalized data structures rather than embedding business logic.

---

# 19. Future Considerations

Version 1.0 deliberately keeps the Scheduling Model generic.

Future implementations may replace OR-Tools with another optimization engine without changing:

* Plan
* PlanVersion
* WorkflowInstance
* OperationInstance
* Assignment

The SchedulingModel remains the stable contract between the Planning Domain and the optimization engine.
