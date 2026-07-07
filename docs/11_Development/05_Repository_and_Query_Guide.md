# docs/11_Development/05_Repository_and_Query_Guide.md

# Development Guide

## Chapter 5 - Repository and Query Guide

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines how persistent data shall be accessed within Lab APS.

Lab APS separates write operations from read operations.

The objective is to:

- Preserve Aggregate boundaries
- Keep Repositories small
- Optimize reporting independently
- Improve long-term maintainability

---

# 2. Design Philosophy

Lab APS adopts a lightweight CQRS approach.

Command Side

↓

Repository

Read Side

↓

Query Service

Both access the same relational database.

No Event Sourcing is required.

---

# 3. Repository Responsibilities

Repositories exist only to persist Aggregate Roots.

Repositories answer the question:

> "How is the Aggregate stored?"

Repositories do **not** answer business questions.

---

# 4. Repository Scope

Every Aggregate Root owns one Repository.

Examples

```text id="rq001"
PlanRepository

EquipmentRepository

StaffRepository

WorkflowDefinitionRepository
```

Repositories never exist for child entities.

Examples

```text id="rq002"
AssignmentRepository

OperationRepository

DemandRepository
```

These are prohibited.

---

# 5. Standard Repository Interface

Every Repository should expose a minimal interface.

Recommended methods

```text id="rq003"
get(id)

save(aggregate)

exists(id)

delete(id)      (only where supported)
```

Optional

```text id="rq004"
find_by_business_code()
```

Avoid exposing arbitrary search methods.

---

# 6. Repository Rules

Repositories shall:

- load Aggregate Roots
- persist Aggregate Roots
- map Domain Objects ↔ ORM Models

Repositories shall not:

- build reports
- implement business rules
- perform scheduling
- perform analytics

---

# 7. Query Services

Query Services answer business questions.

Examples

```text id="rq005"
PlanningDashboardQuery

EquipmentUtilizationQuery

MaterialForecastQuery

PlanListQuery

ExecutionHistoryQuery
```

Query Services are optimized for reading.

---

# 8. Query Characteristics

Query Services may:

- Join multiple tables
- Return DTOs
- Execute optimized SQL
- Read database views

Query Services never return Domain Entities.

---

# 9. Example

Command

```text id="rq006"
GenerateScheduleUseCase

↓

PlanRepository

↓

Save Plan
```

Read

```text id="rq007"
Planning Dashboard

↓

PlanningDashboardQuery

↓

DashboardDTO
```

The two paths remain independent.

---

# 10. Transaction Rules

Repositories participate in transactions.

Query Services do not.

Read operations shall never modify business data.

---

# 11. ORM Mapping

Repositories own ORM mapping.

Query Services may:

- use ORM
- use SQLAlchemy Core
- use optimized SQL

Implementation may vary according to performance requirements.

---

# 12. DTO Policy

Repositories return Domain Objects.

Query Services return DTOs.

The two shall never be mixed.

---

# 13. Performance Strategy

Large datasets should always be retrieved through Query Services.

Examples

- Dashboard
- Gantt Chart
- Historical Reports
- KPI Trends

Repositories shall not become reporting engines.

---

# 14. Architectural Rules

1. One Aggregate Root → One Repository.

2. Child entities are persisted through the Aggregate Root.

3. Repositories are write-oriented.

4. Query Services are read-oriented.

5. Query Services return DTOs only.

6. Business logic belongs to the Domain.

7. Reporting logic belongs to Query Services.

---

# 15. Recommended Package Structure

```text id="rq008"
infrastructure/

    repositories/

        plan_repository.py

        equipment_repository.py

    queries/

        planning_dashboard_query.py

        plan_list_query.py

        equipment_utilization_query.py

        material_forecast_query.py
```

Repositories and Query Services are independent.

---

# 16. Code Review Checklist

Before introducing a new Repository method, verify:

- Is this modifying an Aggregate?
- Could this be implemented as a Query Service?
- Does it return a Domain Object?
- Does it preserve Aggregate boundaries?

If the method primarily answers a reporting or searching question, it belongs in a Query Service rather than a Repository.

---

# 17. Implementation Baseline

Lab APS adopts a lightweight CQRS architecture.

The write model is represented by:

- Domain
- Aggregate
- Repository
- Use Case

The read model is represented by:

- Query Service
- DTO
- API

This separation shall remain throughout the lifetime of the platform.
