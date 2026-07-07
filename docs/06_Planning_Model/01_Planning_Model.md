# docs/06_Planning_Dataset/01_Planning_Dataset.md

# Planning Dataset

## Chapter 1 - Planning Dataset

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the Planning Dataset used by the Planning Engine.

The Planning Dataset is the normalized representation of all information required for one planning execution.

It acts as the canonical input for:

- Scheduling Engine
- Simulation
- Material Forecast
- KPI Analysis

The Planning Dataset is independent of:

- Database schema
- ORM
- OR-Tools
- User Interface

---

# 2. Design Goals

The Planning Dataset shall satisfy the following objectives.

- Immutable
- Deterministic
- Serializable
- Solver-independent
- Reusable
- Testable

The same Planning Dataset shall always produce the same scheduling result under the same Solver Profile.

---

# 3. Dataset Generation Pipeline

The Planning Dataset is generated from business objects.

```text id="pd001"
Laboratory Definition

        │

        ▼

Planning Context

        │

        ▼

PlanVersion

        │

        ▼

Planning Dataset

        │

        ▼

Scheduling Engine
```

The Planning Dataset is generated once per scheduling execution.

---

# 4. Dataset Composition

The Planning Dataset consists of several logical collections.

```text id="pd002"
Planning Dataset

├── Resource Dataset

├── Operation Dataset

├── Calendar Dataset

├── Dependency Dataset

├── Constraint Dataset

└── Objective Dataset
```

Each dataset has a single responsibility.

---

# 5. Resource Dataset

Contains all schedulable resources.

Version 1.0 includes:

- Equipment
- Staff
- Shift

Only scheduling attributes are included.

Business metadata is excluded.

---

# 6. Operation Dataset

Contains all Operation Instances that belong to the current PlanVersion.

Each operation contains only scheduling-relevant information.

Examples

- Duration
- Resource Requirements
- Dependency References
- Priority

---

# 7. Calendar Dataset

Represents effective scheduling availability.

Includes:

- Working Days
- Shift Windows
- Staff Leave
- Equipment Maintenance

Calendar Dataset contains only usable scheduling windows.

---

# 8. Dependency Dataset

Represents execution relationships between operations.

Each dependency contains:

- Predecessor
- Successor
- Relationship Type
- Lag

Dependencies are normalized before entering the Scheduling Engine.

---

# 9. Constraint Dataset

Represents normalized scheduling constraints.

Constraint Dataset is generated automatically from:

- Resource Dataset
- Operation Dataset
- Calendar Dataset
- Planning Policies

Business Rules are never stored directly.

---

# 10. Objective Dataset

Represents optimization objectives.

Examples

- Complete all demand
- Balance workload
- Maximize equipment utilization

Objective weights originate from the Solver Profile.

---

# 11. Dataset Ownership

| Dataset            | Owner             |
| ------------------ | ----------------- |
| Resource Dataset   | Planning Engine   |
| Operation Dataset  | Planning Engine   |
| Calendar Dataset   | Planning Engine   |
| Dependency Dataset | Planning Engine   |
| Constraint Dataset | Scheduling Engine |
| Objective Dataset  | Scheduling Engine |

Planning prepares data.

Scheduling interprets data.

---

# 12. Architectural Rules

1. The Planning Dataset is immutable.
2. The Planning Dataset is generated from one PlanVersion.
3. The Planning Dataset is never persisted.
4. All downstream engines consume the Planning Dataset rather than business entities.
5. New planning capabilities shall extend the dataset instead of bypassing it.

---

# 13. Long-Term Vision

The Planning Dataset becomes the canonical planning representation of Lab APS.

Future capabilities such as:

- Simulation
- AI-assisted planning
- Schedule comparison
- Multi-site optimization
- Scenario analysis

shall consume the same Planning Dataset without introducing alternative input models.
