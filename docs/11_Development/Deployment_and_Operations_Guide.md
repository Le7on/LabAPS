# Deployment and Operations Guide

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Status:** Draft

---

## 1. Purpose

This guide describes the expected deployment model and the operational considerations for running Lab APS in development and future deployment environments.

---

## 2. Target Runtime Model

The current architecture separates the application into:

- backend services for domain logic and planning workflows
- frontend SPA for the user interface
- shared persistence layer for planning and configuration data

The implementation baseline expects the backend to expose REST endpoints and the frontend to consume them through a clear API boundary.

---

## 3. Development Run Model

### Backend

The backend is expected to run as a Python service using Flask and application modules under the backend tree.

Suggested development flow:

```bash
python -m flask --app backend.app run
```

### Frontend

The frontend is expected to run as a Vue 3 application with Vite.

Suggested development flow:

```bash
npm install
npm run dev
```

---

## 4. Environment Configuration

The project should use environment-based configuration for:

- database connection settings
- solver profile settings
- logging options
- feature flags

The bootstrap templates already reference environment support through a dotenv-style configuration approach.

---

## 5. Database Considerations

The architecture baseline expects:

- SQLite for development
- PostgreSQL for future production use
- Alembic-managed migrations

Operational guidance:

- keep schema changes tied to domain changes
- validate migrations before release
- treat published planning data as immutable

---

## 6. Logging and Monitoring

The system should produce structured logs for:

- plan creation
- scheduling execution
- planning version publication
- errors in solver execution
- API failures

Monitoring should cover both application health and scheduling workflow completion.

---

## 7. Release Checklist

Before deployment, confirm:

- the relevant architecture and requirements docs are current
- the database migration scripts are validated
- test suites pass
- environment variables are configured
- the frontend build succeeds
- the backend starts without import errors

---

## 8. Operational Risks to Watch

The most important operational risks are:

- solver failures during schedule generation
- inconsistent planning context snapshots
- invalid state transitions for plan versions
- stale or missing configuration data

These areas should be covered by monitoring, validation checks, and explicit error handling.

---

## 9. Recommended Next Step

Start with a local development deployment path first, then add CI-oriented validation and production deployment steps as the implementation matures.
