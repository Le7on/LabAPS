# docs/09_UI/04_Plan_Workspace_Design.md

# User Interface Design

## Chapter 4 - Plan Workspace Design

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the primary workspace used by the Production Laboratory Manager.

The Plan Workspace is the central working environment of Lab APS.

Rather than navigating between independent pages, users perform the complete planning lifecycle within a single contextual workspace.

This workspace is centered on one **Plan Version**.

---

# 2. Design Philosophy

The user should always know:

- Which Plan is currently open.
- Which Plan Version is currently being edited.
- What planning stage has been completed.
- What action should be performed next.

The workspace minimizes context switching.

---

# 3. Workspace Overview

```text
+--------------------------------------------------------------------------------------+
| Week 32 Production Plan                                      Version 3 (Working)     |
| Planning Horizon: 2026-W32                                   Solver Profile: Default |
+--------------------------------------------------------------------------------------+

 Demand | Schedule | Forecast | KPI | Versions | Activity

----------------------------------------------------------------------------------------

                           Current Workspace

----------------------------------------------------------------------------------------

[ Primary Content ]

----------------------------------------------------------------------------------------

Generate Schedule     Publish     Compare Version     Export
```

The current Plan remains visible at all times.

---

# 4. Workspace Sections

Every Plan Workspace consists of six sections.

| Section       | Purpose                            |
| ------------- | ---------------------------------- |
| Header        | Current planning context           |
| Navigation    | Workspace tabs                     |
| Content       | Active business view               |
| Warning Panel | Validation and scheduling warnings |
| Action Bar    | Business actions                   |
| Status Bar    | Current planning state             |

---

# 5. Workspace Header

The header always displays the planning identity.

Required information

- Plan Name
- Planning Horizon
- Current Version
- Version Type
- Plan Status

Optional information

- Planner
- Last Updated
- Solver Profile

The header never scrolls.

---

# 6. Workspace Tabs

The workspace uses business-oriented tabs.

```text
Demand

Schedule

Forecast

KPI

Versions

Activity
```

Each tab represents one aspect of the current Plan Version.

Tabs never navigate to another Plan.

---

# 7. Demand View

Purpose

Define production demand.

Typical information

- Project
- Quantity
- Priority

Available actions

- Add Demand
- Edit Demand
- Remove Demand

Demand editing is allowed only while the Plan Version is editable.

---

# 8. Schedule View

Purpose

Display generated assignments.

Recommended layout

- Timeline (Gantt)
- Equipment View
- Staff View

Users may switch between views without leaving the workspace.

Schedule generation is initiated from this view.

---

# 9. Forecast View

Purpose

Display expected material consumption.

Typical information

- Material Summary
- Daily Consumption
- Weekly Consumption
- Inventory Warnings (if available)

Forecast is read-only.

---

# 10. KPI View

Purpose

Evaluate planning quality.

Recommended metrics

- Demand Completion
- Equipment Utilization
- Staff Utilization
- Solver Runtime

KPIs are regenerated after every scheduling execution.

---

# 11. Version View

Purpose

Manage Plan Versions.

Typical information

- Version Number
- Version Type
- Status
- Created Time
- Comment

Available actions

- Create Version
- Compare Version
- Publish Version

Historical versions remain read-only.

---

# 12. Activity View

Purpose

Display the planning history.

Examples

- Version Created
- Schedule Generated
- Published
- Archived

Activity provides audit visibility.

It is not an execution log.

---

# 13. Warning Panel

Warnings remain visible regardless of the active tab.

Typical warnings

- No feasible schedule
- Material shortage
- Missing capability
- Missing qualification
- Calendar conflict

Warnings are categorized as:

- Information
- Warning
- Blocking Error

Blocking errors prevent publication.

---

# 14. Action Bar

The Action Bar contains the primary business actions.

Version 1.0

```text
Generate Schedule

Publish

Export
```

Secondary actions

```text
Compare

Archive

Refresh
```

Business actions remain visible regardless of the active tab.

---

# 15. Workspace States

The workspace reflects the current Plan Version state.

Examples

Draft

Generate Schedule enabled

Publish disabled

Published

Generate Schedule disabled

Publish disabled

Execution available

The UI shall never allow actions that violate the Plan lifecycle.

---

# 16. Context Preservation

The current Plan Version is preserved while switching tabs.

Examples

```text
Week 32

Version 3

Demand

↓

Forecast

↓

KPI
```

The user never loses planning context.

---

# 17. Design Rules

1. One workspace represents one Plan Version.

2. Users never edit multiple Plan Versions simultaneously.

3. Planning context is always visible.

4. Business actions remain accessible.

5. Tabs organize information, not navigation.

6. Warnings are persistent.

7. The Plan Workspace remains the primary screen throughout the planning lifecycle.

---

# 18. Future Extension

Future tabs may include:

```text
Scenario

Simulation

AI Recommendation

Constraint Analysis

Solver Diagnostics
```

The Plan Workspace shall remain the primary interaction model for future planning capabilities.

New functionality should extend the existing workspace rather than introducing separate planning pages.
