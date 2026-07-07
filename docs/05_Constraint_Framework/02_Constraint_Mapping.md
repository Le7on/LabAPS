# docs/05_Constraint_Framework/02_Constraint_Mapping.md

# Constraint Framework

## Chapter 2 - Constraint Mapping

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines how Business Rules are transformed into scheduling constraints.

The objective is to completely separate:

- Laboratory business rules
- Scheduling implementation
- Solver implementation

Business Rules shall never be translated directly into OR-Tools constraints.

Instead, they are progressively transformed into normalized scheduling concepts.

---

# 2. Transformation Pipeline

Every scheduling rule follows the same transformation pipeline.

```text id="cm001"
Business Rule

↓

Rule Interpreter

↓

Constraint Specification

↓

Constraint Builder

↓

Constraint Model

↓

Solver Adapter

↓

Solver Constraint
```

Each stage has one responsibility.

---

# 3. Stage Responsibilities

## Business Rule

Represents laboratory knowledge.

Example

```text id="cm002"
384 PNG requires 384 Head.
```

Business Rules are written using laboratory language.

Business Rules never mention solver concepts.

---

## Rule Interpreter

The Rule Interpreter classifies Business Rules.

It determines:

- Constraint Category
- Source Object
- Target Object
- Parameters

The Rule Interpreter performs classification only.

It performs no scheduling.

---

## Constraint Specification

Constraint Specification is the normalized representation of one scheduling rule.

Example

```text id="cm003"
Category

Capability

Source

OperationInstance

Target

Equipment

Requirement

384 Head
```

Constraint Specifications are immutable.

---

## Constraint Builder

Constraint Builder converts specifications into solver-independent constraints.

Responsibilities include:

- Resolve references
- Resolve snapshots
- Validate completeness
- Normalize values

Constraint Builder never invokes OR-Tools.

---

## Constraint Model

Constraint Model groups all normalized constraints.

Example

```text id="cm004"
Constraint Model

├── Capability Constraints
├── Resource Constraints
├── Dependency Constraints
├── Calendar Constraints
└── Policy Constraints
```

The model contains only scheduling concepts.

---

## Solver Adapter

The Solver Adapter converts the Constraint Model into solver-specific constraints.

The Solver Adapter owns all OR-Tools APIs.

No business terminology shall appear inside the Solver Adapter.

---

# 4. Mapping Principles

The following principles apply.

### Principle 1

One Business Rule may generate multiple Constraint Specifications.

---

### Principle 2

Different Business Rules may generate the same Constraint Category.

---

### Principle 3

Constraint Categories remain stable.

Business Rules evolve.

---

### Principle 4

Constraint Specifications shall be deterministic.

The same Business Rule shall always generate the same specifications.

---

# 5. Mapping Examples

## Example 1

Business Rule

```text id="cm005"
384 PNG requires 384 Head.
```

Mapping

```text id="cm006"
Business Rule

↓

Capability Constraint Specification

↓

Capability Constraint

↓

Solver
```

---

## Example 2

Business Rule

```text id="cm007"
One Equipment executes only one Operation at a time.
```

Mapping

```text id="cm008"
Business Rule

↓

Resource Constraint Specification

↓

Resource Constraint

↓

Solver
```

---

## Example 3

Business Rule

```text id="cm009"
SAP starts after SMDP.
```

Mapping

```text id="cm010"
Business Rule

↓

Dependency Constraint Specification

↓

Dependency Constraint

↓

Solver
```

---

## Example 4

Business Rule

```text id="cm011"
Equipment must pass FV before production.
```

Mapping

```text id="cm012"
Business Rule

↓

Qualification Constraint Specification

↓

Qualification Constraint

↓

Solver
```

---

# 6. Composite Rules

Some Business Rules generate multiple Constraint Specifications.

Example

```text id="cm013"
SMDP Output Plate

supports multiple SAP

within shelf life

limited by stamp-out count
```

Possible mapping

```text id="cm014"
Dependency Constraint

+

Policy Constraint

+

Resource Constraint (Future)
```

One Business Rule may therefore participate in multiple scheduling dimensions.

---

# 7. Constraint Resolution

Constraint Builder resolves references before creating the Constraint Model.

Typical resolution steps include:

- Resolve OperationInstance
- Resolve Equipment Capability
- Resolve Staff Skill
- Resolve Planning Context
- Resolve Calendar Windows

After resolution, the Constraint Model contains only normalized scheduling objects.

---

# 8. Validation

Constraint Specifications shall be validated before scheduling.

Validation includes:

- Missing references
- Invalid parameters
- Unsupported categories
- Inconsistent dependencies

Invalid specifications prevent Scheduling Model creation.

The Solver shall never receive invalid constraints.

---

# 9. Mapping Ownership

| Stage                    | Owner               |
| ------------------------ | ------------------- |
| Business Rule            | Laboratory Business |
| Rule Interpreter         | Planning Domain     |
| Constraint Specification | Planning Domain     |
| Constraint Builder       | Scheduling Engine   |
| Constraint Model         | Scheduling Engine   |
| Solver Constraint        | Solver Adapter      |

Responsibilities never overlap.

---

# 10. Extensibility

Adding a new Business Rule follows this workflow.

```text id="cm015"
New Business Rule

↓

Determine Constraint Category

↓

Create Constraint Specification

↓

Existing Constraint Builder

↓

Constraint Model

↓

Solver
```

Only if an existing Constraint Category cannot express the new rule shall the Constraint Framework itself be extended.

---

# 11. Architectural Rules

1. Business Rules shall never generate solver constraints directly.

2. Rule Interpreter shall classify but never optimize.

3. Constraint Specifications are immutable.

4. Constraint Builder shall remain solver-independent.

5. Constraint Model shall contain only normalized scheduling concepts.

6. Solver Adapter is the only component allowed to generate OR-Tools constraints.

7. Mapping logic shall be deterministic and repeatable.

---

# 12. Relationship to Future Business Rules

The Constraint Framework is intentionally generic.

Future laboratory rules should be introduced by:

- adding new Business Rules,
- mapping them to existing Constraint Categories,
- extending Constraint Specifications where necessary.

The framework itself should evolve slowly, while Business Rules may evolve continuously with laboratory operations.
