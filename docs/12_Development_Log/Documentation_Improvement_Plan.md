# Documentation Improvement Plan

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Review Date:** 2026-07-07

**Scope:** Full review of the documentation set under the docs directory.

---

# 1. Summary Assessment

The current documentation set is already strong in architecture coverage. It provides a clear vision, requirements baseline, architecture design, ADRs, planning model, state model, database design, UI design, API design, and development workflow guidance.

The main gap is not missing domain knowledge, but rather documentation consistency, navigation, and alignment with the actual repository progress.

---

# 2. Strengths Observed

The documentation already has several strengths:

* Clear business and architecture separation.
* Strong ADR discipline.
* Good domain modeling coverage.
* Comprehensive planning and scheduling design.
* A visible development workflow and engineering baseline.

These are valuable assets for a long-term platform project.

---

# 3. Main Issues Identified

## 3.1 Inconsistent document references

Some documents still point to artifact paths that do not match the actual file layout.

Example:

* The project context refers to a planned path under docs/07_Database/01_Physical_ERD.md, but the current database folder contains 03_Physical_ERD.md.

This creates avoidable confusion for contributors.

## 3.2 Naming inconsistency

The file name 01_Bussiness_Capability.md uses a non-standard spelling of “Business”.

This should be normalized for consistency and discoverability.

## 3.3 Documentation is comprehensive but not yet navigable

The repository contains many strong documents, but there is no single entry page that explains:

* which documents should be read first,
* which ones are authoritative,
* which ones are implementation-ready,
* which ones are still pending or draft.

## 3.4 Architecture docs are ahead of implementation status

The documentation describes the target architecture very clearly, but the repository state appears to be in an earlier bootstrap stage. The docs should explicitly distinguish:

* architecture baseline,
* current implementation status,
* next implementation milestones.

## 3.5 Missing operational documentation

The current set covers architecture and design well, but the following are still weak or missing from the practical developer experience:

* local setup instructions,
* environment bootstrapping,
* test strategy and validation steps,
* deployment runbook,
* contribution workflow.

---

# 4. Recommended Improvements

## Priority 0 — Immediate

1. Add a top-level documentation entry page.
   - A single file such as docs/README.md or a clearly linked summary page would improve onboarding.

2. Add a documentation status matrix.
   - Each document should show status: Draft, Baseline, Frozen, Implemented, Pending.

3. Fix path and filename inconsistencies.
   - Align references to actual files.
   - Normalize the document naming convention.

4. Add a “current implementation status” section to the architecture index.
   - This should explain which design artifacts are implemented, which are pending, and which are only conceptual.

## Priority 1 — Near Term

5. Add a requirement-to-design-to-implementation traceability matrix.
   - Link requirements, ADRs, architecture documents, and code modules.

6. Add a developer onboarding guide.
   - Include setup steps for backend, frontend, tests, and tooling.

7. Add a testing and validation guide.
   - Define unit test strategy, integration test strategy, and acceptance criteria.

8. Add a release and change management note.
   - This should describe how architecture changes, documentation updates, and implementation changes are coordinated.

## Priority 2 — Medium Term

9. Introduce documentation governance rules.
   - Each major change should update the related documents in the same change set.

10. Create a lightweight document template.
   - Standard metadata should include: owner, version, status, last updated, related ADRs, and related modules.

---

# 5. Suggested Document Changes by Area

## Vision and Requirements

* Keep the vision and SRS as-is, but add a short “current implementation status” note at the top of each major document.

## Architecture

* Add a one-page architecture snapshot for new contributors.
* Keep ADRs, but add a short summary section for each ADR linking to the relevant implementation module.

## Database and API

* Add a status note saying whether each artifact is design-only or implementation-ready.
* Add examples of how the documented model maps to the actual project modules.

## UI and Frontend

* Add a frontend architecture note that explains the Vue 3 SPA structure and how it relates to the backend API.
* Add a simple page map for the planned user workspace.

## Development and Operations

* Add setup and run instructions.
* Add testing and deployment guidance.
* Add a changelog or milestone log linked to the development plan.

---

# 6. Recommended Next Step

The next practical step should be to create a documentation index and implementation status map, then update the existing architecture index so that the repository becomes easier to navigate for both new and returning contributors.
