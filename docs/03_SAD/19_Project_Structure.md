# docs/03_SAD/19_Project_Structure.md

# Software Architecture Design

## Chapter 19 - Project Structure

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the physical project structure of Lab APS.

The project structure shall mirror the Domain Architecture.

Folders are organized by business responsibility rather than technical framework.

---

# 2. Design Principles

The project structure follows the following principles.

1. Domain drives structure.
2. Engines are reusable.
3. Infrastructure is isolated.
4. Use Cases coordinate business actions.
5. Repository implementations remain private.
6. OR-Tools exists only inside the Solver module.

---

# 3. Project Layout

```text
lab_aps/

├── app.py
├── config.py
├── requirements.txt
├── migrations/
├── tests/
├── docs/
│
├── application/
│   ├── planning/
│   ├── laboratory/
│   ├── execution/
│   └── reporting/
│
├── domain/
│   ├── laboratory/
│   ├── planning/
│   ├── execution/
│   └── common/
│
├── engines/
│   ├── workflow/
│   ├── planning/
│   ├── scheduling/
│   ├── assignment/
│   └── material/
│
├── solver/
│   ├── builder/
│   ├── adapter/
│   ├── constraints/
│   ├── objectives/
│   └── models/
│
├── infrastructure/
│   ├── persistence/
│   ├── repositories/
│   ├── orm/
│   ├── logging/
│   └── export/
│
├── api/
│
├── ui/
│   ├── templates/
│   ├── static/
│   └── assets/
│
└── shared/
    ├── exceptions/
    ├── enums/
    ├── value_objects/
    └── utils/
```

---

# 4. application/

The Application Layer contains Use Cases.

Example

```text
application/planning/

├── create_plan.py
├── create_plan_version.py
├── generate_schedule.py
├── publish_plan.py
├── archive_plan.py
└── compare_versions.py
```

Each file implements one business use case.

Application modules coordinate domain behavior.

They do not implement business rules.

---

# 5. domain/

The Domain Layer contains business concepts.

```text
domain/planning/

├── aggregates/
├── entities/
├── services/
├── policies/
└── events/
```

Example

```text
aggregates/

Plan.py
```

```text
entities/

PlanVersion.py

WorkflowInstance.py

OperationInstance.py

Assignment.py
```

```text
services/

WorkflowGenerator.py

PlanValidator.py
```

The Domain Layer contains no Flask or SQLAlchemy dependencies.

---

# 6. engines/

Engines implement reusable algorithms.

Current engines

```text
workflow/

WorkflowGenerator.py
```

```text
planning/

PlanningContextBuilder.py

PlanningValidator.py
```

```text
scheduling/

SchedulingModelBuilder.py

AssignmentBuilder.py
```

```text
material/

MaterialCalculator.py
```

Engines are stateless.

They may be reused by multiple Use Cases.

---

# 7. solver/

The Solver module encapsulates optimization.

```text
solver/

builder/

adapter/

constraints/

objectives/

models/
```

Responsibilities

builder/

Create optimization variables.

constraints/

Convert scheduling constraints.

objectives/

Build optimization objectives.

adapter/

Wrap OR-Tools.

models/

Internal scheduling model.

The rest of the application shall never import OR-Tools directly.

---

# 8. infrastructure/

Infrastructure implements technical details.

Contains

```text
repositories/

orm/

persistence/

logging/

export/
```

Infrastructure depends on external libraries.

Business logic is prohibited.

---

# 9. api/

The API layer adapts HTTP requests to Use Cases.

Suggested structure

```text
api/

planning.py

laboratory.py

execution.py

reporting.py
```

Routes remain thin.

Validation and orchestration occur in the Application Layer.

---

# 10. ui/

The desktop interface.

Contains

* HTML
* Bootstrap
* JavaScript
* Static assets

Business logic shall not exist in the UI.

---

# 11. tests/

Testing mirrors the production structure.

```text
tests/

application/

domain/

engines/

solver/

integration/
```

Every module shall have a corresponding test package.

---

# 12. Dependency Rules

Allowed

```text
api

↓

application

↓

domain

↓

engines

↓

solver

↓

infrastructure
```

Infrastructure supports every layer but does not own business behavior.

Forbidden

* domain → api
* domain → infrastructure
* engines → api
* solver → repository
* ui → domain

---

# 13. Shared Components

The `shared` package contains only generic cross-cutting concepts.

Allowed

* Exceptions
* Enumerations
* Value Objects
* Generic utilities

Forbidden

* Business entities
* Business services
* Scheduling logic

If a class is specific to Planning or Laboratory Definition, it shall belong to that domain instead of `shared`.

---

# 14. Import Rules

Every import shall move inward toward the Domain.

Example

```text
API
    ↓
Application
    ↓
Domain
    ↓
Engine
    ↓
Solver
```

Circular imports are prohibited.

---

# 15. Evolution Strategy

New functionality shall be added by extending existing modules.

Examples

Future feature

Scenario Planning

Implementation

```text
application/planning/create_scenario.py

domain/planning/entities/Scenario.py
```

The existing structure shall remain unchanged.

---

# 16. Architecture Checklist

Before adding a new file, developers shall answer:

1. Which Domain owns this class?
2. Is this a Use Case, Entity, Engine or Infrastructure component?
3. Does this introduce a new dependency?
4. Can an existing Engine be reused?
5. Does the location reflect the business responsibility?

If these questions cannot be answered clearly, the design should be reviewed before implementation.
