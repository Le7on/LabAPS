# docs/06_Planning_Dataset/02_Scheduling_Model.md

# Planning Dataset

## Chapter 2 - Scheduling Model

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the Scheduling Model.

The Scheduling Model is the internal optimization model used by the Scheduling Engine.

It is generated from the Planning Dataset.

It is consumed by the Solver Adapter.

The Scheduling Model is **not** a business model.

It is **not** a persistence model.

It is **not** exposed outside the Scheduling Engine.

---

# 2. Position in Architecture

The complete planning pipeline is shown below.

```text
Laboratory Definition
        │
        ▼
Planning Domain
        │
        ▼
Planning Dataset
        │
        ▼
Scheduling Model Builder
        │
        ▼
Scheduling Model
        │
        ▼
Solver Adapter
        │
        ▼
Scheduling Solution
```

The Scheduling Model exists only during optimization.

---

# 3. Responsibilities

The Scheduling Model is responsible for:

* Normalizing planning data
* Preparing optimization objects
* Holding optimization variables
* Holding normalized constraints
* Holding optimization objectives

The Scheduling Model is NOT responsible for:

* Business validation
* Workflow generation
* Database persistence
* Material calculation

---

# 4. Model Composition

The Scheduling Model consists of five logical parts.

```text
Scheduling Model

├── Resource Graph

├── Operation Graph

├── Constraint Model

├── Objective Model

└── Variable Model
```

Each part has a single responsibility.

---

# 5. Resource Graph

The Resource Graph represents all schedulable resources.

Version 1.0 supports:

* Equipment
* Staff
* Shift

Resources contain only scheduling attributes.

Business information has already been removed.

---

# 6. Operation Graph

Operation Graph represents executable work.

Each node is an Operation Instance.

Each edge is a dependency.

Example

```text
SMDP

↓

SAP
```

The graph is a scheduling structure rather than a workflow definition.

---

# 7. Variable Model

Variable Model represents optimization variables.

Typical variables include:

* Assignment Variable
* Start Variable
* End Variable

Variables are created after the Scheduling Model is fully constructed.

Variables never exist in the Planning Dataset.

---

# 8. Constraint Model

Constraint Model contains normalized scheduling constraints.

Categories include:

* Resource Constraints
* Capability Constraints
* Qualification Constraints
* Dependency Constraints
* Calendar Constraints
* Policy Constraints

Constraint Model contains scheduling semantics only.

It contains no OR-Tools objects.

---

# 9. Objective Model

Objective Model defines optimization goals.

Examples

* Maximize completed demand
* Balance workload
* Maximize equipment utilization

Objective weights originate from the Solver Profile.

Objectives are independent from Constraints.

---

# 10. Scheduling Solution

The Solver returns a Scheduling Solution.

Scheduling Solution contains:

* Assignment Results
* Objective Score
* Solver Runtime
* Diagnostics

Scheduling Solution contains no Domain Objects.

---

# 11. Builder Responsibilities

The Scheduling Engine consists of the following builders.

```text
Planning Dataset

↓

SchedulingModelBuilder

↓

VariableBuilder

↓

ConstraintBuilder

↓

ObjectiveBuilder

↓

SolverAdapter
```

Each builder transforms one layer into the next.

Builders shall not skip layers.

---

# 12. Architectural Rules

1. Planning Dataset shall never contain Variables.

2. Planning Dataset shall never contain Constraints.

3. Planning Dataset shall never contain Objectives.

4. Scheduling Model owns Variables.

5. Scheduling Model owns Constraints.

6. Scheduling Model owns Objectives.

7. OR-Tools receives only the Scheduling Model.

8. Business entities never enter the Scheduling Engine.

---

# 13. Design Philosophy

The architecture deliberately separates planning from optimization.

Planning answers:

> What needs to be scheduled?

Scheduling answers:

> How should it be optimized?

Solver answers:

> What is the best feasible solution?

Maintaining these boundaries ensures that business evolution and optimization evolution remain independent.
