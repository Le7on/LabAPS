# docs/03_SAD/06_Application_Architecture.md

# Software Architecture Design

## Chapter 6 - Application Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the Application Layer of Lab APS.

The Application Layer coordinates business use cases.

It does not contain business rules.

It does not perform optimization.

It does not access the user interface directly.

Its responsibility is orchestration.

---

# 2. Architectural Position

```text
Presentation Layer
        │
        ▼
Application Layer
        │
        ▼
Domain Layer
        │
        ▼
Infrastructure Layer
```

The Application Layer is the only layer that coordinates multiple domains.

---

# 3. Responsibilities

The Application Layer is responsible for:

* Executing use cases
* Transaction management
* Repository coordination
* Calling Domain Services
* Calling Infrastructure Services
* Returning DTOs to Presentation

The Application Layer shall never:

* Implement business rules
* Build optimization models
* Query OR-Tools directly
* Contain SQL

---

# 4. Application Services

The following Application Services are defined.

```text
PlanApplicationService

PlanningApplicationService

SchedulingApplicationService

ExecutionApplicationService

ReportingApplicationService

LaboratoryApplicationService
```

Each service represents a business use case rather than a database entity.

---

# 5. PlanApplicationService

Responsible for Plan lifecycle management.

Supported use cases:

* Create Plan
* Copy Plan
* Load Plan
* Publish Plan
* Archive Plan
* Create New Version

Input

* Planning Horizon
* Plan Name

Output

* Plan DTO

---

# 6. PlanningApplicationService

Responsible for coordinating planning.

Supported use cases:

* Validate Planning Context
* Generate Workflow Instances
* Generate Operations
* Calculate Material Forecast
* Calculate KPI

Typical workflow

```text
Load Plan

↓

Validate

↓

Generate Workflow

↓

Generate Operations

↓

Return Updated Plan
```

This service does not invoke the Solver.

---

# 7. SchedulingApplicationService

Responsible for scheduling execution.

Supported use cases:

* Generate Schedule
* Recalculate Schedule
* Validate Schedule

Typical workflow

```text
Load Plan

↓

Convert To Scheduling Model

↓

Scheduling Engine

↓

Assignments

↓

Save Plan
```

---

# 8. ExecutionApplicationService

Responsible for execution management.

Supported use cases:

* Start Assignment
* Complete Assignment
* Update Assignment Status
* Complete Plan

Execution never modifies scheduling decisions.

---

# 9. ReportingApplicationService

Responsible for report generation.

Supported use cases:

* Equipment Utilization
* Staff Utilization
* Material Forecast Report
* Weekly Planning Report

Reports are generated from published Plans.

---

# 10. LaboratoryApplicationService

Responsible for laboratory configuration.

Supported use cases:

* Manage Staff
* Manage Equipment
* Manage Capability
* Manage Skills
* Manage Shift
* Manage Holidays
* Manage Maintenance

This service belongs to the Foundation Domain.

---

# 11. Application Workflow

The complete scheduling workflow is shown below.

```text
User

↓

Create Plan

↓

Generate Workflow

↓

Generate Schedule

↓

Calculate Material Forecast

↓

Review

↓

Publish

↓

Execute
```

Each step corresponds to one Application Service method.

---

# 12. Repository Access Rules

Repositories are accessed only by the Application Layer.

Example

```text
Application Service

↓

Plan Repository

↓

Plan Aggregate
```

The Presentation Layer shall never access repositories.

The Domain Layer shall never access repositories directly.

---

# 13. Transaction Boundary

Each Application Service method defines one transaction.

Example

Create Plan

Transaction

Validate

↓

Create Plan

↓

Save Plan

↓

Commit

If any step fails, the transaction shall be rolled back.

---

# 14. DTO Design

The Application Layer exchanges DTOs with the Presentation Layer.

Example DTOs

```text
PlanSummaryDTO

PlanDetailDTO

ScheduleDTO

AssignmentDTO

EquipmentDTO

StaffDTO
```

Domain entities shall never be returned directly to the UI.

---

# 15. Dependency Rules

Allowed dependencies

```text
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

Forbidden dependencies

* Presentation → Domain
* Presentation → Repository
* Domain → Flask
* Domain → SQLAlchemy
* Domain → OR-Tools

---

# 16. Error Handling

Application Services convert internal exceptions into business responses.

Examples

Validation Error

```text
Missing Equipment Capability
```

Scheduling Error

```text
No Feasible Solution
```

Execution Error

```text
Assignment Already Completed
```

Unexpected exceptions shall be logged by Infrastructure.

---

# 17. Security Boundary

Authentication and authorization are enforced by the Application Layer.

Typical authorization examples

* Planner may publish Plans.
* Operator may update Assignment status.
* Engineer may modify Workflow Templates.
* Administrator may modify laboratory configuration.

Authorization rules shall not exist in the Presentation Layer.

---

# 18. Service Naming Convention

Application Services shall always be named using business capabilities.

Correct

```text
PlanApplicationService

SchedulingApplicationService

ReportingApplicationService
```

Avoid

```text
PlanManager

SchedulerManager

CommonService

UtilityService
```

Business-oriented naming improves maintainability.

---

# 19. Future Extension

Future services may include

* ScenarioApplicationService
* NotificationApplicationService
* AuditApplicationService
* IntegrationApplicationService

Existing Application Services shall remain stable.

New business capabilities shall be introduced through new services rather than modifying existing ones.
