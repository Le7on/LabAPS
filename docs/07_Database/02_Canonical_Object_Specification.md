# docs/07_Database/02_Canonical_Object_Specification.md

# Canonical Object Specification

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the canonical specification for every business object in Lab APS.

While the Canonical Data Model defines relationships between objects, this document defines the internal structure and ownership of each object.

Every implementation shall derive its data definition from this specification.

This document is independent of:

* Database
* ORM
* REST API
* JSON
* Programming Language

---

# 2. Object Specification Template

Every canonical object shall be described using the same structure.

Each object defines:

* Purpose
* Owner
* Identity
* Business Attributes
* Relationships
* Mutable Attributes
* Derived Attributes
* Lifecycle

This template shall be used consistently throughout the project.

---

# 3. Object Categories

Canonical objects are grouped into four categories.

```text
Definition Objects

Planning Objects

Result Objects

Execution Objects
```

Each category follows different lifecycle rules.

---

# 4. Plan

## Purpose

Represents one business planning identity.

Example

Week 32 Production Plan

---

## Owner

Planning Domain

---

## Identity

Technical

* UUID

Business

* Plan Code

---

## Business Attributes

* Name
* Planning Horizon
* Description

---

## Relationships

Owns

* Plan Versions

References

None

---

## Mutable Attributes

* Name
* Description

Planning Horizon becomes immutable after the first Plan Version is created.

---

## Derived Attributes

Current Published Version

Number of Versions

---

## Lifecycle

Active

↓

Archived

---

# 5. Plan Version

## Purpose

Represents one complete scheduling result.

---

## Owner

Plan

---

## Identity

UUID

Version Number

---

## Business Attributes

* Version Type
* Status
* Solver Runtime
* Objective Score

---

## Relationships

Owns

* Planning Context
* Demand
* Workflow Instances
* Assignments
* Material Forecast
* KPI

---

## Mutable Attributes

Status

Review Information

Until Published.

After publication the object becomes immutable.

---

## Derived Attributes

Assignment Count

Operation Count

Completion Percentage

---

## Lifecycle

Working

↓

Reviewed

↓

Published

↓

Archived

---

# 6. Planning Context

## Purpose

Represents the immutable planning environment.

---

## Owner

Plan Version

---

## Business Attributes

* Calendar Snapshot
* Equipment Availability Snapshot
* Staff Availability Snapshot
* Shift Profile
* Solver Profile

---

## Mutable Attributes

None

Planning Context is immutable after creation.

---

## Derived Attributes

None

---

# 7. Workflow Instance

## Purpose

Represents one generated execution of a Workflow Definition.

---

## Owner

Plan Version

---

## Business Attributes

* Business Code
* Status

---

## Relationships

Owns

* Operation Instances

References

* Workflow Definition

---

## Mutable Attributes

Status

---

## Derived Attributes

Operation Count

Completion Percentage

---

# 8. Operation Instance

## Purpose

Represents the smallest executable planning object.

---

## Owner

Workflow Instance

---

## Business Attributes

* Operation Type
* Duration
* Status

---

## Relationships

References

* Operation Definition

Owns

None

---

## Mutable Attributes

Execution Status

---

## Derived Attributes

Scheduling State

Completion State

---

# 9. Assignment

## Purpose

Represents one scheduling allocation.

---

## Owner

Plan Version

---

## Business Attributes

* Planned Start
* Planned End
* Status

---

## Relationships

References

* Operation Instance
* Equipment
* Staff
* Shift

---

## Mutable Attributes

Execution Status

Only execution updates are permitted after publication.

---

## Derived Attributes

Duration

Execution Delay

---

# 10. Material Forecast

## Purpose

Represents predicted material consumption.

---

## Owner

Plan Version

---

## Business Attributes

* Material
* Quantity
* Warning Level

---

## Mutable Attributes

None

Material Forecast is regenerated whenever scheduling is regenerated.

---

## Derived Attributes

Consumption Summary

Inventory Warning

---

# 11. KPI

## Purpose

Represents calculated planning indicators.

---

## Owner

Plan Version

---

## Business Attributes

None

KPI values are system-generated.

---

## Derived Attributes

* Equipment Utilization
* Staff Utilization
* Completion Rate
* Solver Runtime

---

# 12. Specification Rules

Every canonical object follows the rules below.

1. Identity is immutable.

2. Ownership never changes.

3. Mutable attributes are explicitly defined.

4. Derived attributes are never persisted unless justified by performance.

5. Business relationships are independent of database implementation.

6. Runtime optimization objects never appear in this specification.

---

# 13. Implementation Mapping

This specification is the direct input for:

* Physical ERD
* SQLAlchemy Models
* DTO Definitions
* OpenAPI Schemas
* Import/Export Models

No implementation may redefine object structure independently.

---

# 14. Architecture Baseline

The Canonical Object Specification becomes the definitive description of all business objects in Lab APS.

Future changes to object structure require both:

* an Architecture Decision Record (ADR)
* an update to this document

This ensures long-term consistency across the entire platform.
