# docs/09_UI/05_Plan_Workspace_Wireframe.md

# User Interface Design

## Chapter 5 - Plan Workspace Wireframe

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the primary planning workspace of Lab APS.

The Plan Workspace is the main working area for the Production Laboratory Manager.

Every planning activity begins and ends in this workspace.

---

# 2. Design Objectives

The workspace shall allow users to:

* Understand the current planning status immediately.
* Perform the complete planning lifecycle without changing pages.
* Focus on one Plan Version at a time.
* Review scheduling results before publication.

---

# 3. Overall Layout

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ Lab APS                                                     User      Notifications         │
├──────────────┬───────────────────────────────────────────────────────────────────────────────┤
│ Dashboard    │ Week 32 Production Plan                                               Draft  │
│ Planning     │ Planning Horizon : 2026-W32                                            V3    │
│ Resources    │ Solver Profile   : Default                                              LM01  │
│ Processes    ├───────────────────────────────────────────────────────────────────────────────┤
│ Execution    │ Demand | Schedule | Forecast | KPI | Versions | Activity                    │
│ Reports      ├───────────────────────────────────────────────────────────────────────────────┤
│ Admin        │                                                                               │
│              │                                                                               │
│              │                     Active Workspace                                          │
│              │                                                                               │
│              │                                                                               │
│              │                                                                               │
│              ├───────────────────────────────────────────────────────────────────────────────┤
│              │ Warnings / Messages                                                          │
│              ├───────────────────────────────────────────────────────────────────────────────┤
│              │ Generate Schedule | Publish | Compare | Export | Refresh                     │
└──────────────┴───────────────────────────────────────────────────────────────────────────────┘
```

---

# 4. Layout Zones

The workspace consists of six fixed areas.

## Global Navigation

Purpose

Navigate between business domains.

Contents

* Dashboard
* Planning
* Resources
* Processes
* Execution
* Reports
* Administration

This navigation remains visible throughout the application.

---

## Plan Header

Purpose

Display the current planning context.

Fields

* Plan Name
* Planning Horizon
* Current Version
* Version Type
* Plan Status
* Solver Profile

The header is always visible.

---

## Workspace Tabs

Purpose

Switch between planning views.

Tabs

* Demand
* Schedule
* Forecast
* KPI
* Versions
* Activity

Tabs never change the current Plan Version.

---

## Active Workspace

Purpose

Display business content.

Only one workspace is active at any time.

---

## Warning Panel

Purpose

Display planning issues.

Categories

* Information
* Warning
* Blocking Error

Blocking errors prevent publication.

Warnings remain visible regardless of the active tab.

---

## Action Bar

Purpose

Expose primary business actions.

Primary

* Generate Schedule
* Publish

Secondary

* Compare Version
* Export
* Refresh

Actions change according to Plan Version status.

---

# 5. Demand Workspace

```text
Demand
──────────────────────────────────────────────────────────────

+-----------------------------------------------------------+
| Project          Quantity        Priority                  |
+-----------------------------------------------------------+
| FV                    6          Normal                    |
| 96 OPA               12          Normal                    |
| 384 PNG              20          High                      |
| AZ RSV                8          Normal                    |
+-----------------------------------------------------------+

[ Add ] [ Edit ] [ Remove ]
```

The planner edits production demand only in this view.

---

# 6. Schedule Workspace

The Schedule view provides three interchangeable layouts.

## Equipment View

```text
HM01

Shift1   OPA001

Shift2   OPA002
```

---

## Staff View

```text
Tom

Shift1   PNG001

Shift2   FV001
```

---

## Timeline (Gantt)

```text
Equipment

HM09

████ PNG001 ████

████ PNG002 ████

HM10

████ FV001 ████
```

The user may switch views without regenerating the schedule.

---

# 7. Forecast Workspace

```text
Material Forecast

------------------------------------------------------

Material              Required      Warning

384 Tips                2400

384 Plate                 20

Deepwell Block            20

FV Kit                     6
```

Inventory values are optional.

Warnings are highlighted when available.

---

# 8. KPI Workspace

Recommended KPI cards.

```text
Completion Rate

98%

Equipment Utilization

87%

Staff Utilization

82%

Solver Runtime

5.2 sec
```

Charts may be added in future versions.

---

# 9. Version Workspace

```text
Version

Status

Type

Created

V1

Archived

Working

2026-07-01

V2

Archived

Working

2026-07-02

V3

Published

Published

2026-07-03
```

Available actions

* Compare
* Clone
* Publish

Only one version may be Published.

---

# 10. Activity Workspace

Displays chronological planning history.

Example

```text
09:10

Plan Created

09:22

Schedule Generated

09:24

Material Forecast Updated

09:30

Published
```

The Activity view supports auditing and troubleshooting.

---

# 11. Responsive Behaviour

The desktop application targets 1920×1080 resolution.

Minimum supported resolution

1366×768

The left navigation remains fixed.

The workspace expands with available width.

---

# 12. UI Design Rules

1. One Plan Version occupies one workspace.

2. The planner shall never lose planning context.

3. Business actions remain visible at all times.

4. Navigation changes modules, not planning context.

5. Tabs change information views, not business objects.

6. Every action produces visible feedback.

7. Planning remains the visual center of the application.
