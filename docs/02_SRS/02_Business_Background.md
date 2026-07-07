# docs/02_SRS/02_Business_Background.md

# Software Requirements Specification

## Chapter 2 - Business Background

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This chapter describes the laboratory business environment and explains why Lab APS is required.

The objective is to establish a common understanding of the current planning process, identify existing business problems and define the scope of optimization.

This chapter focuses on **business operations**, not software implementation.

---

# 2. Laboratory Overview

The laboratory operates multiple automated workstations capable of executing different testing projects.

Each workstation has different hardware configurations and therefore different capabilities.

Examples include:

- Different Head Types
- Different Channel Configurations
- Different Supported Projects

Laboratory operators also possess different qualifications and may only perform specific operations on specific equipment.

Laboratory production is therefore constrained by both equipment capability and operator qualification.

---

# 3. Current Planning Process

Laboratory production follows a weekly planning cycle.

The planning process begins with production demand from the Principal Investigator (PI).

The Production Laboratory Manager converts this demand into an executable production schedule.

The current workflow is illustrated below.

```text
Principal Investigator
        │
        │ Weekly Production Demand
        ▼
Production Laboratory Manager
        │
        │ Manual Planning
        ▼
Equipment Assignment
        │
        ▼
Operator Assignment
        │
        ▼
Schedule Review
        │
        ▼
Laboratory Execution
```

Most planning activities are currently performed manually.

---

# 4. Business Participants

The planning process involves five major roles.

## Principal Investigator (PI)

Responsibilities

- Define weekly production demand
- Determine production priorities
- Approve production objectives

The PI does not perform scheduling.

---

## Production Laboratory Manager

Responsibilities

- Create production plans
- Assign resources
- Execute scheduling
- Review planning results
- Publish production plans

This role is the primary user of Lab APS.

---

## Laboratory Engineer

Responsibilities

- Configure laboratory resources
- Maintain workflow templates
- Maintain equipment information
- Maintain operator qualifications

Engineers provide configuration data used during planning.

---

## Operator

Responsibilities

- Execute assigned laboratory operations
- Report execution status

Operators do not create schedules.

---

## System Administrator

Responsibilities

- Maintain user accounts
- Maintain permissions
- Maintain system configuration

---

# 5. Business Objects

The planning process revolves around several business objects.

## Production Demand

Represents production requirements for a planning period.

Provided by the PI.

Example

| Project | Required Runs |
| ------- | ------------: |
| FV      |             6 |
| 96 OPA  |            12 |
| 384 PNG |            18 |

---

## Workflow

Represents the execution process required to complete a laboratory project.

Each Project is associated with exactly one Workflow Template.

---

## Operation

Represents the smallest executable laboratory activity.

Operations are the units scheduled by Lab APS.

Examples

- FV
- SMDP
- SAP
- CP
- SP

---

## Assignment

Represents the allocation of:

- Operation
- Equipment
- Staff
- Shift

Assignments are generated automatically by the Scheduler.

---

## Plan

Represents the complete scheduling result for a planning period.

A Plan includes:

- Demand
- Workflow Instances
- Assignments
- Material Forecast

---

# 6. Business Constraints

The laboratory follows several operational constraints.

Examples include:

## Equipment Constraints

Equipment capability determines which operations may be executed.

Example

384 Head operations cannot be assigned to 96 Head equipment.

---

## Qualification Constraints

Equipment must satisfy qualification requirements before production.

Example

FV qualification must remain valid before production work can begin.

---

## Personnel Constraints

Operators may only perform operations for which they possess the required skills.

---

## Calendar Constraints

Scheduling must respect:

- Working Days
- Holidays
- Leave
- Equipment Maintenance
- Shift Definitions

---

## Workflow Constraints

Workflow execution order must always be respected.

Example

```text
SMDP

↓

SAP
```

---

# 7. Current Business Challenges

The current planning process experiences several operational challenges.

## BC-001

Manual planning consumes significant time.

---

## BC-002

Resource conflicts are difficult to detect.

---

## BC-003

Workflow dependencies increase scheduling complexity.

---

## BC-004

Changes to production demand often require the entire schedule to be recreated.

---

## BC-005

Equipment maintenance and staff leave require manual schedule adjustments.

---

## BC-006

Material consumption must be calculated manually after planning.

---

## BC-007

Equipment utilization is difficult to evaluate objectively.

---

## BC-008

Planning quality depends heavily on individual experience.

---

# 8. Business Opportunities

Lab APS introduces several improvements.

## Automated Planning

Automatically generate executable production schedules.

---

## Standardized Planning

Ensure consistent planning regardless of planner experience.

---

## Constraint Validation

Automatically verify:

- Equipment Capability
- Operator Qualification
- Workflow Dependencies
- Equipment Qualification
- Calendar Availability

---

## Material Forecast

Automatically estimate material consumption after schedule generation.

---

## Resource Analysis

Provide utilization analysis for:

- Equipment
- Operators

---

## Planning Traceability

Maintain complete planning history and published plans.

---

# 9. Business Scope

The responsibilities of Lab APS are clearly defined.

## Lab APS Is Responsible For

- Production Planning
- Resource Allocation
- Schedule Optimization
- Workflow Scheduling
- Material Forecast
- Planning Analysis

---

## Lab APS Is NOT Responsible For

- Sample Management
- Laboratory Results
- Inventory Management
- Instrument Control
- Purchasing
- Financial Management
- ERP Functions

These functions remain external to Lab APS.

---

# 10. Business Vision

The long-term objective is to transform laboratory planning from an experience-driven activity into a standardized and reproducible business process.

The desired future workflow is illustrated below.

```text
Production Demand
        │
        ▼
Generate Plan
        │
        ▼
Automatic Scheduling
        │
        ▼
Review & Adjust
        │
        ▼
Publish Plan
        │
        ▼
Laboratory Execution
        │
        ▼
Material Forecast & Analysis
```

Lab APS becomes the central planning platform connecting production demand with laboratory execution while remaining independent of laboratory execution systems.
