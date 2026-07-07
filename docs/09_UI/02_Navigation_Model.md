# docs/09_UI/02_Navigation_Model.md

# User Interface Design

## Chapter 2 - Navigation Model

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the navigation model of Lab APS.

The objective is to ensure that users can complete their daily work with minimal navigation effort.

Navigation is designed around laboratory workflows rather than technical modules.

---

# 2. Navigation Philosophy

Navigation follows one simple principle.

> Users should navigate according to what they are trying to accomplish.

The application therefore organizes functions around laboratory activities instead of database entities.

---

# 3. Primary Navigation

Version 1.0 consists of seven primary modules.

```text id="nav001"
Dashboard

Planning

Resources

Processes

Execution

Reports

Administration
```

The navigation order follows the lifecycle of laboratory production.

---

# 4. Dashboard

Purpose

Provide an overview of laboratory status.

Typical widgets

* Current Planning Horizon
* Published Plan
* Equipment Alerts
* Material Warnings
* Today's Execution
* Recent Activities

Typical user

Everyone

---

# 5. Planning

Purpose

Create and manage production plans.

Navigation

```text id="nav002"
Planning

├── Plans

├── Plan Versions

├── Demand

├── Schedule

├── Material Forecast

└── KPI
```

Typical user

Production Laboratory Manager

Planning is expected to occupy approximately 80% of daily usage.

---

# 6. Resources

Purpose

Maintain physical laboratory resources.

Navigation

```text id="nav003"
Resources

├── Staff

├── Equipment

├── Skills

├── Capabilities

└── Materials
```

Resources describe **what the laboratory owns**.

Typical user

Laboratory Engineer

---

# 7. Processes

Purpose

Maintain reusable laboratory process definitions.

Navigation

```text id="nav004"
Processes

├── Projects

├── Workflow Definitions

├── Operation Definitions

├── Shift

└── Calendar
```

Processes describe **how laboratory work is performed**.

These settings affect future planning only.

Historical planning remains unchanged.

---

# 8. Execution

Purpose

Track execution of published plans.

Navigation

```text id="nav005"
Execution

├── Assignment Board

├── Execution Status

└── Execution History
```

Execution is read/write.

Planning data remains read-only.

---

# 9. Reports

Purpose

Analyze planning and execution.

Navigation

```text id="nav006"
Reports

├── Planning

├── Equipment

├── Staff

├── Material Forecast

└── KPI
```

Reports never modify business data.

---

# 10. Administration

Purpose

Maintain application configuration.

Navigation

```text id="nav007"
Administration

├── Users

├── Roles

├── Solver Profiles

├── Audit Log

└── System Settings
```

Business configuration belongs elsewhere.

Administration is system-oriented.

---

# 11. Secondary Navigation

Each primary module follows a consistent pattern.

```text id="nav008"
List

↓

Detail

↓

Action

↓

Result
```

Example

```text id="nav009"
Plans

↓

Week 32 Plan

↓

Generate Schedule

↓

Review

↓

Publish
```

The user always knows the current context.

---

# 12. Breadcrumb Rules

Every page shall display its location.

Example

```text id="nav010"
Planning

>

Week 32 Plan

>

Version 3

>

Schedule
```

Breadcrumbs improve navigation inside deeply nested planning objects.

---

# 13. Context Preservation

Switching between modules shall preserve context whenever possible.

Example

Current context

```text id="nav011"
Week 32

Version 3
```

When opening

Equipment

and returning to Planning,

the user returns to

```text id="nav012"
Week 32

Version 3
```

instead of the Planning list.

---

# 14. Navigation Rules

1. Every business object has one primary entry point.

2. Editing occurs in exactly one location.

3. Reports remain read-only.

4. Execution never edits Planning.

5. Resources and Processes affect future planning only.

6. Dashboard provides navigation, not editing.

7. Planning remains the center of daily operations.

---

# 15. Future Navigation

Future modules shall integrate into the existing hierarchy.

Examples

```text id="nav013"
Planning

├── Scenario Planning

├── Simulation

└── AI Recommendation
```

```text id="nav014"
Reports

├── Trend Analysis

└── Historical Comparison
```

The primary navigation should remain stable even as functionality grows.
