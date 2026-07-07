# docs/11_Development/02_Project_Structure_Implementation.md

# Development Guide

## Chapter 2 - Project Structure Implementation

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines the physical source code organization of Lab APS.

The project structure mirrors the business architecture and runtime architecture defined in previous documents.

The objective is to ensure that every developer places code in the correct location with consistent responsibilities.

---

# 2. Design Principles

The source code organization follows these principles.

1. Business domains determine package boundaries.
2. Use Cases coordinate business actions.
3. Engines implement reusable algorithms.
4. Infrastructure is isolated.
5. Frameworks remain at the outermost layer.

---

# 3. Repository Layout

```text
lab-aps/

├── app.py
├── run.py
├── pyproject.toml
├── requirements.txt
├── alembic.ini
├── migrations/
├── docs/
├── tests/
│
├── application/
│
├── domain/
│
├── engines/
│
├── infrastructure/
│
├── api/
│
├── ui/
│
├── config/
│
└── shared/
```

Each top-level package owns one responsibility.

---

# 4. application/

The Application Layer contains business use cases.

```text
application/

    planning/

        create_plan.py

        create_plan_version.py

        generate_schedule.py

        approve_plan_version.py

        publish_plan_version.py

    resources/

    execution/

    reporting/
```

Rules

- One file implements one Use Case.
- No ORM code.
- No SQL.
- No OR-Tools.

---

# 5. domain/

The Domain Layer contains business concepts.

```text
domain/

    planning/

        aggregates/

        entities/

        services/

        events/

    laboratory/

    execution/

    common/
```

Examples

Aggregates

- Plan

Entities

- PlanVersion
- WorkflowInstance
- OperationInstance
- Assignment

Services

- PlanningContextBuilder
- WorkflowGenerator

Rules

- Pure Python only.
- No Flask.
- No SQLAlchemy.
- No OR-Tools.

---

# 6. engines/

The Engines implement reusable planning algorithms.

```text
engines/

    planning/

        planning_problem_builder.py

        planning_context_builder.py

        workflow_generator.py

    scheduling/

        scheduling_model_builder.py

        constraint_builder.py

        objective_builder.py

        assignment_builder.py

    material/

        material_calculator.py
```

Rules

- Stateless.
- Reusable.
- No persistence.

---

# 7. solver/

The Solver package encapsulates optimization implementation.

```text
solver/

    adapter/

    model/

    variables/

    constraints/

    objectives/

    solution/
```

Responsibilities

- Variable generation
- Constraint translation
- Objective translation
- Solver execution
- Solution parsing

Only this package may import OR-Tools.

---

# 8. infrastructure/

Infrastructure contains implementation details.

```text
infrastructure/

    persistence/

    orm/

    repositories/

    logging/

    export/

    services/
```

Responsibilities

- SQLAlchemy
- Alembic
- File export
- Logging
- External integrations

Business logic is prohibited.

---

# 9. api/

The API layer adapts HTTP requests to Use Cases.

```text
api/

    planning.py

    resources.py

    execution.py

    reports.py
```

Responsibilities

- Request parsing
- DTO conversion
- HTTP response
- Authentication hooks

No business logic.

---

# 10. ui/

Desktop presentation.

```text
ui/

    templates/

    static/

        css/

        js/

        img/

    assets/
```

Responsibilities

- HTML
- JavaScript
- Bootstrap
- Icons

The UI never accesses repositories directly.

---

# 11. config/

Configuration files.

```text
config/

    config.yaml

    logging.yaml

    solver.yaml
```

Business configuration is stored in the database.

Application configuration is stored here.

---

# 12. shared/

Shared contains cross-cutting components only.

Allowed

- Exceptions
- Enums
- Value Objects
- Generic utilities

Forbidden

- Business entities
- Use Cases
- Scheduling logic

---

# 13. Dependency Rules

Allowed

```text
API

↓

Application

↓

Domain

↓

Engines

↓

Solver

↓

Infrastructure
```

Forbidden

- Domain → Infrastructure
- Domain → API
- Solver → Repository
- UI → Domain
- Engines → ORM

---

# 14. File Naming Convention

Python modules

```text
snake_case.py
```

Classes

```text
PascalCase
```

Functions

```text
snake_case()
```

Use Cases

```text
create_plan.py

generate_schedule.py

publish_plan_version.py
```

Engine classes

```text
PlanningProblemBuilder

SchedulingModelBuilder

ConstraintBuilder
```

---

# 15. Implementation Rules

1. One responsibility per module.
2. One Aggregate per repository.
3. One business action per Use Case.
4. One transaction per Use Case.
5. Engines are stateless.
6. Runtime models are never persisted.
7. Domain objects remain framework-independent.

---

# 16. Code Review Checklist

Before merging code, verify:

- Is the code placed in the correct package?
- Does it introduce an illegal dependency?
- Does it duplicate an existing Engine?
- Does it violate Aggregate boundaries?
- Does it expose ORM models outside Infrastructure?
- Does it introduce business logic outside the Domain?

Only code satisfying all checks may be merged.

---

# 17. Development Baseline

This project structure is the standard implementation model for Lab APS Version 1.0.

All future modules shall follow this organization unless an Architecture Decision Record explicitly approves a structural change.
