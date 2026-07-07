# docs/09_UI/06_Interaction_Specification.md

# User Interface Design

## Chapter 6 - Interaction Specification

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the interaction behaviour of the Lab APS user interface.

Unlike the Wireframe, which defines layout, this document defines how the application responds to user actions.

The goal is to provide a predictable and consistent user experience.

---

# 2. Interaction Principles

The user interface follows these principles.

### Principle 1

Every user action produces visible feedback.

---

### Principle 2

Long-running operations display progress.

---

### Principle 3

The interface always reflects the current Plan Version.

---

### Principle 4

Business actions are explicit.

The system shall never perform hidden business operations.

---

### Principle 5

The current planning context shall never be lost.

---

# 3. Generate Schedule

## Trigger

User selects

```text id="is001"
Generate Schedule
```

---

## UI Behaviour

Immediately after clicking

* Disable Generate button.
* Disable Demand editing.
* Display progress indicator.
* Display current pipeline step.

Example

```text id="is002"
Generating Schedule...

✔ Validate Planning Context

✔ Build Planning Problem

✔ Build Scheduling Model

⏳ Optimizing...

□ Build Assignments

□ Calculate Forecast

□ Calculate KPI
```

---

## Completion

When scheduling completes

* Refresh Schedule View.
* Refresh Forecast.
* Refresh KPI.
* Enable Generate button.
* Enable Publish button (if validation succeeds).

---

# 4. Publish Plan Version

## Trigger

User selects

```text id="is003"
Publish
```

---

## Confirmation

Display confirmation dialog.

Example

```text id="is004"
Publish Version 3?

This action will make the version read-only.

[ Cancel ]

[ Publish ]
```

---

## Success

Display notification.

```text id="is005"
Plan Version Published Successfully.
```

Refresh

* Version List
* Header
* Dashboard

---

# 5. Version Switching

When the user selects another Plan Version

The system reloads:

* Demand
* Schedule
* Forecast
* KPI
* Activity

The current workspace tab remains unchanged.

Example

```text id="is006"
Schedule

↓

Version 2

↓

Schedule
```

The user does not lose workspace context.

---

# 6. Demand Editing

Demand editing is allowed only while the current Plan Version is editable.

After publication

The Demand tab becomes read-only.

Buttons

```text id="is007"
Add

Edit

Remove
```

are disabled automatically.

---

# 7. Warning Behaviour

Warnings remain visible until resolved.

Categories

Information

Blue

Warning

Yellow

Blocking Error

Red

Blocking Errors disable:

* Publish

Warnings do not disable scheduling unless configured by policy.

---

# 8. Validation Feedback

Validation occurs before scheduling.

Example

```text id="is008"
Planning Context Validation

✔ Equipment

✔ Staff

✖ Workflow Definition

Missing Workflow Definition

PNG
```

The user may navigate directly to the related configuration page.

---

# 9. Save Behaviour

Configuration pages use explicit saving.

Workflow

```text id="is009"
Edit

↓

Save

↓

Confirmation
```

Automatic saving is not supported in Version 1.0.

---

# 10. Navigation Behaviour

Changing modules preserves the current planning context whenever possible.

Example

```text id="is010"
Planning

↓

Resources

↓

Planning
```

Returns to

```text id="is011"
Week 32

Version 3

Schedule
```

The planner never loses work unexpectedly.

---

# 11. Loading Behaviour

Data loading shall display placeholders rather than empty pages.

Examples

* Loading Plan
* Loading Schedule
* Loading Report

The application shall remain responsive while loading.

---

# 12. Error Behaviour

Business errors are displayed inline.

Example

```text id="is012"
No feasible schedule found.

Please review:

• Equipment Availability

• Workflow Dependencies
```

Unexpected system errors display a generic message.

Detailed information is written to the application log.

---

# 13. Unsaved Changes

If the user attempts to leave a page containing unsaved changes

Display confirmation.

Example

```text id="is013"
You have unsaved changes.

Leave this page?

[ Stay ]

[ Leave ]
```

---

# 14. Refresh Behaviour

Only the active workspace is refreshed after business actions.

Example

Generate Schedule

Refresh

* Schedule
* Forecast
* KPI

Do not reload the entire application.

---

# 15. Interaction Rules

1. Every business action has visible feedback.

2. The current Plan Version is always visible.

3. Long-running actions display progress.

4. Navigation preserves user context.

5. Read-only states are enforced visually.

6. Validation feedback is actionable.

7. Business errors are understandable.

8. System errors are recoverable where possible.

---

# 16. Future Interaction

Future versions may introduce:

* Background scheduling
* Live progress updates
* Compare Versions side-by-side
* AI recommendations
* Drag-and-drop manual adjustment

These features shall extend the existing interaction model without changing the primary planning workflow.
