# docs/02_SRS/04_Functional_Requirements.md

# Software Requirements Specification

## Chapter 4 - Functional Requirements

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This chapter defines the functional capabilities that shall be provided by Lab APS.

Each functional requirement (FR) is uniquely identified and shall be traceable to:

- Business Process
- Software Architecture Design (SAD)
- REST API
- Test Cases

---

# 2. Functional Capability Map

Lab APS consists of the following business capabilities.

```text
Lab APS

├── Master Data Management
├── Configuration Management
├── Planning Management
├── Workflow Management
├── Scheduling
├── Execution
├── Material Forecast
└── Reporting
```

Each capability is described below.

---

# 3. Master Data Management

Master Data defines the static information of the laboratory.

## FR-MD-001 Staff Management

The system shall manage laboratory staff information.

Functions include:

- Create Staff
- Update Staff
- Disable Staff
- View Staff

---

## FR-MD-002 Staff Skill Management

The system shall maintain operator skills.

Each Staff member may possess multiple Skills.

Examples

- FV
- 96 OPA
- 384 PNG
- AZ RSV
- DiLA

---

## FR-MD-003 Equipment Management

The system shall manage laboratory equipment.

Equipment properties include:

- Name
- Equipment Type
- Capability
- Status
- Enable Flag

---

## FR-MD-004 Equipment Capability

The system shall maintain equipment capabilities.

Capabilities describe hardware characteristics rather than projects.

Examples

- 96 Head
- 384 Head
- 16 Channel
- 14 Channel
- iSWAP

Operations shall match required capabilities.

---

## FR-MD-005 Project Management

The system shall manage laboratory Projects.

Each Project references one Workflow Template.

---

## FR-MD-006 Workflow Template Management

The system shall support configurable Workflow Templates.

A Workflow Template consists of:

- Operations
- Dependencies
- Intermediate Outputs
- Material BOM

Workflow Templates are reusable.

---

## FR-MD-007 Material BOM Management

The system shall maintain material consumption definitions.

Material BOM is defined at Operation level.

Material BOM shall not participate in scheduling optimization.

---

# 4. Configuration Management

Configuration controls laboratory operation.

## FR-CFG-001 Shift Configuration

The system shall support configurable Shift definitions.

Each Shift contains:

- Name
- Start Time
- End Time

---

## FR-CFG-002 Holiday Calendar

The system shall maintain laboratory holidays.

Holidays shall be excluded from scheduling.

---

## FR-CFG-003 Staff Leave

The system shall maintain planned staff leave.

Leave shall affect scheduling availability.

---

## FR-CFG-004 Equipment Maintenance

The system shall maintain planned equipment maintenance.

Maintenance shall affect equipment availability.

---

## FR-CFG-005 Solver Parameters

The system shall maintain scheduling parameters.

Examples

- Planning Horizon
- Solver Timeout
- Optimization Strategy

---

# 5. Planning Management

Planning is the core capability of Lab APS.

## FR-PLAN-001 Create Plan

The system shall create a new Plan.

A Plan includes:

- Planning Horizon
- Demand
- Status

---

## FR-PLAN-002 Maintain Demand

The system shall maintain production demand.

Demand consists of:

- Project
- Required Quantity
- Priority (Optional)

---

## FR-PLAN-003 Validate Planning Inputs

Before scheduling, the system shall validate:

- Staff Availability
- Equipment Availability
- Calendar
- Workflow Configuration

Validation errors shall prevent scheduling.

---

## FR-PLAN-004 Generate Workflow Instances

The system shall convert Demand into Workflow Instances.

Workflow generation shall be automatic.

---

## FR-PLAN-005 Generate Operations

Workflow Instances shall be expanded into executable Operations.

Operations become scheduling units.

---

## FR-PLAN-006 Review Plan

The system shall allow planners to review generated schedules before publication.

---

## FR-PLAN-007 Publish Plan

The system shall publish approved Plans.

Only Published Plans may enter execution.

---

## FR-PLAN-008 Version Management

The system shall support multiple Plan versions.

Only one version may be Published.

---

# 6. Scheduling

Scheduling allocates Operations to laboratory resources.

## FR-SCH-001 Generate Schedule

The system shall generate an executable schedule automatically.

---

## FR-SCH-002 Allocate Equipment

The scheduler shall assign suitable equipment to each Operation.

Equipment Capability shall satisfy Operation requirements.

---

## FR-SCH-003 Allocate Staff

The scheduler shall assign qualified staff.

Required Skills shall be validated.

---

## FR-SCH-004 Allocate Shift

Every Assignment shall belong to exactly one Shift.

---

## FR-SCH-005 Workflow Dependency

Workflow dependencies shall always be respected.

Example

```text
SMDP

↓

SAP
```

---

## FR-SCH-006 Equipment Qualification

Equipment shall satisfy qualification requirements before assignment.

Example

Equipment requiring FV must have a valid FV status.

---

## FR-SCH-007 Conflict Detection

The scheduler shall prevent:

- Equipment conflicts
- Staff conflicts
- Shift conflicts

---

## FR-SCH-008 Recalculate Schedule

Draft or Reviewed Plans may be recalculated.

Published Plans shall not be modified.

---

# 7. Execution

Execution records actual laboratory progress.

## FR-EXE-001 Assignment Status

Assignments shall support status updates.

Examples

- Not Started
- Running
- Completed
- Failed

---

## FR-EXE-002 Plan Status

Plan status shall be updated according to Assignment progress.

---

# 8. Material Forecast

Material Forecast is generated after scheduling.

## FR-MAT-001 Calculate Material Consumption

The system shall calculate expected material usage based on the generated Schedule.

---

## FR-MAT-002 Material Summary

The system shall summarize consumption by:

- Material
- Day
- Week

---

## FR-MAT-003 Inventory Verification

The system shall compare forecast consumption with available inventory when inventory information is provided.

The system shall generate warnings only.

Inventory quantities shall not be modified.

---

# 9. Reporting

## FR-RPT-001 Schedule Report

The system shall export generated schedules.

Supported formats

- Excel
- PDF (Future)

---

## FR-RPT-002 Material Forecast Report

The system shall export material consumption summaries.

---

## FR-RPT-003 Resource Utilization Report

The system shall provide utilization reports for:

- Equipment
- Staff

---

# 10. Dashboard

## FR-DASH-001 Planning Dashboard

The dashboard shall display:

- Current Plans
- Plan Status
- Weekly Demand
- Published Plans

---

## FR-DASH-002 Resource Dashboard

The dashboard shall display:

- Equipment Status
- Staff Availability
- Qualification Alerts

---

## FR-DASH-003 Material Dashboard

The dashboard shall display:

- Forecast Consumption
- Material Warnings

---

# 11. Requirement Traceability

Each functional requirement shall map to:

- Business Process
- Business Rules
- Use Cases
- Software Architecture
- Test Cases

Example

| Requirement | Related Business Process    |
| ----------- | --------------------------- |
| FR-PLAN-004 | Generate Workflow Instances |
| FR-SCH-005  | Workflow Dependency         |
| FR-MAT-001  | Material Forecast           |

This traceability shall be maintained throughout the project lifecycle.
