# docs/04_ADR/ADR-008-Planning-Context-Uses-Snapshots.md

# ADR-008 — Planning Context Uses Snapshots Instead of Live References

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

A production plan is generated using the current laboratory configuration.

The laboratory configuration continuously changes.

Examples include:

* Staff leave
* Equipment maintenance
* Holiday calendar
* Shift definition
* Solver parameters

If a PlanVersion references the current configuration directly, historical planning results may become impossible to reproduce.

Example

Week 32

```text
Tom

Working
```

Week 35

```text
Tom

On Leave
```

Opening Week 32 again should still show Tom as available.

The historical planning result must not change because today's configuration changed.

---

# Decision

Every PlanVersion owns one immutable Planning Context.

Planning Context stores **snapshots** of all information required for scheduling.

Planning Context shall never depend on live laboratory configuration after a PlanVersion has been generated.

---

# Planning Context Contents

Planning Context contains:

* Calendar Snapshot
* Shift Snapshot
* Staff Availability Snapshot
* Equipment Availability Snapshot
* Solver Profile Snapshot
* Planning Parameters Snapshot

It intentionally does **not** contain complete copies of Staff or Equipment master data.

Only scheduling-relevant information is stored.

---

# Rationale

## Reproducibility

Running the same PlanVersion years later should produce the same scheduling model.

Snapshots guarantee deterministic behaviour.

---

## Auditability

Planning decisions can always be explained using the exact planning environment that existed when the schedule was generated.

---

## Version Isolation

Each PlanVersion owns its own Planning Context.

Different PlanVersions of the same Plan may therefore use different planning environments.

Example

```text
Week 32

Version 1

↓

HM09 Available

Version 2

↓

HM09 Under Maintenance
```

Both versions remain valid historical records.

---

## Independence from Master Data

Laboratory Definition continues to evolve.

Planning Context freezes only the information required for planning.

Master Data remains the source of truth for future planning.

Planning Context becomes the source of truth for historical planning.

---

# Alternatives Considered

## Option A — Live References

Rejected.

Historical planning would change whenever:

* Staff changed
* Equipment changed
* Calendar changed

Historical schedules would no longer be trustworthy.

---

## Option B — Full Database Copy

Rejected.

Copying all laboratory tables into every PlanVersion would create excessive duplication.

Most master data is irrelevant once scheduling begins.

---

## Option C — Scheduling Snapshot

Accepted.

Capture only planning-relevant scheduling information.

This provides deterministic behaviour with acceptable storage cost.

---

# Consequences

Positive

* Deterministic scheduling.
* Complete audit trail.
* Version independence.
* Reliable comparison between PlanVersions.

Negative

* Additional storage.
* Snapshot generation step during planning.

These costs are considered acceptable.

---

# Architectural Rules

1. Every PlanVersion owns exactly one Planning Context.

2. Planning Context is immutable after schedule generation.

3. Planning Context stores scheduling data, not complete master data.

4. Historical PlanVersions never read current laboratory configuration.

5. SchedulingModelBuilder reads Planning Context rather than Laboratory Definition.

---

# Related Documents

* ADR-001 — Plan as the Aggregate Root
* ADR-002 — Plan + Plan Version
* SAD Chapter 8 — Plan Lifecycle
* SAD Chapter 9 — Plan Version Architecture
* SAD Chapter 14 — Solver Model

---

# Future Considerations

Future versions may optimise snapshot storage using structured JSON or differential snapshots.

Such optimisations shall remain transparent to the Domain Model.

The Planning Context concept shall remain unchanged.
