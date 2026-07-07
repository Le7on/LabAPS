# docs/09_UI/03_User_Flow.md

# User Interface Design

## Chapter 3 - User Flow

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the primary user workflows of Lab APS.

A User Flow describes how users accomplish business goals using the system.

The objective is to optimize user experience while preserving business correctness.

This document is independent of visual design.

---

# 2. Primary Personas

Version 1.0 defines five primary personas.

| Role                          | Primary Goal                     |
| ----------------------------- | -------------------------------- |
| Principal Investigator (PI)   | Define production demand         |
| Production Laboratory Manager | Create, review and publish plans |
| Laboratory Engineer           | Maintain laboratory definitions  |
| Operator                      | Execute assigned work            |
| Administrator                 | Maintain system configuration    |

Each user flow is optimized for one primary persona.

---

# 3. Overall Business Flow

The complete business lifecycle is shown below.

```text
Dashboard

↓

Planning

↓

Generate Schedule

↓

Review

↓

Publish

↓

Execution

↓

Reports
```

Planning is the primary workflow.

---

# 4. Production Laboratory Manager Flow

This is the most important workflow in the system.

```text
Dashboard

↓

Planning

↓

Select Plan

↓

Create Plan Version

↓

Review Planning Context

↓

Review Demand

↓

Generate Schedule

↓

Review Schedule

↓

Review Material Forecast

↓

Review KPI

↓

Publish

↓

Done
```

The workflow is intentionally linear.

The user always knows the next step.

---

# 5. Create New Weekly Plan

Trigger

A new planning horizon begins.

Flow

```text
Dashboard

↓

Create Plan

↓

Enter Planning Horizon

↓

Save

↓

Plan Created
```

Output

A new Plan exists.

No Plan Version exists yet.

---

# 6. Generate Schedule

Trigger

Planner requests scheduling.

Flow

```text
Select Plan

↓

Create Plan Version

↓

Validate Planning Context

↓

Generate Schedule

↓

Review Results
```

System Activities

- Build Planning Problem
- Build Scheduling Model
- Execute Solver
- Generate Assignments
- Calculate Material Forecast
- Calculate KPI

The planner interacts only with the business process.

Internal scheduling steps remain invisible.

---

# 7. Review Schedule

After scheduling, the planner reviews the result.

Review sequence

```text
Schedule

↓

Warnings

↓

Equipment Allocation

↓

Staff Allocation

↓

Material Forecast

↓

KPI
```

If the planner is not satisfied,

a new Plan Version may be generated.

The previous version remains unchanged.

---

# 8. Publish Plan

Trigger

Planner accepts the schedule.

Flow

```text
Review

↓

Publish

↓

Confirmation

↓

Published
```

Effects

- Version becomes immutable.
- Execution becomes available.
- Previous Published Version is retired.

---

# 9. Laboratory Engineer Flow

Purpose

Maintain reusable laboratory definitions.

Typical workflow

```text
Resources

↓

Equipment

↓

Update Capability

↓

Save
```

or

```text
Processes

↓

Workflow Definition

↓

Create New Version

↓

Activate
```

These changes affect only future planning.

Existing Plan Versions remain unchanged.

---

# 10. Operator Flow

Purpose

Execute published assignments.

Workflow

```text
Dashboard

↓

Today's Assignments

↓

Start

↓

Complete

↓

Next Assignment
```

Operators never access planning functionality.

---

# 11. Administrator Flow

Purpose

Maintain application behaviour.

Typical workflow

```text
Administration

↓

Users

↓

Roles

↓

Solver Profiles

↓

Save
```

Business data is not managed here.

---

# 12. Replanning Flow

Replanning does not overwrite existing planning.

Workflow

```text
Open Plan

↓

Create New Version

↓

Modify Demand (optional)

↓

Generate Schedule

↓

Review

↓

Publish
```

Historical versions remain available.

---

# 13. Exception Flow

If scheduling fails.

```text
Generate Schedule

↓

Validation Failed

↓

Display Errors

↓

Correct Configuration

↓

Generate Again
```

No partial schedule is created.

---

# 14. Warning Flow

Warnings do not block planning.

Example

```text
Material Shortage

↓

Display Warning

↓

Planner Reviews

↓

Continue or Cancel
```

Warnings are informational unless explicitly configured as blocking policies.

---

# 15. Navigation Rules

Users should never need to:

- search for the next action
- remember hidden state
- edit the same business object in multiple locations

Each workflow should require as few steps as possible while preserving business correctness.

---

# 16. Design Principles

The UI follows these principles.

1. One screen, one responsibility.

2. One workflow, one primary goal.

3. Planning remains the central experience.

4. Configuration is separated from execution.

5. Every action produces a visible business result.

6. Users think in Plans and Versions, not in database objects.

7. Solver complexity remains hidden behind business language.

---

# 17. Future Workflows

Future versions may extend existing workflows.

Examples

```text
Planning

↓

Scenario

↓

Compare

↓

Publish
```

or

```text
Generate Schedule

↓

AI Recommendation

↓

Planner Decision

↓

Publish
```

Future workflows should extend the existing planning lifecycle rather than replacing it.
