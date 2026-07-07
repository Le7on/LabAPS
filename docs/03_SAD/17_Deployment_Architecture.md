# docs/03_SAD/17_Deployment_Architecture.md

# Software Architecture Design

## Chapter 17 - Deployment Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the deployment architecture of Lab APS.

The deployment architecture describes how software components are packaged, deployed and executed.

Deployment concerns infrastructure only.

It shall not affect the Domain Model.

---

# 2. Design Goals

The deployment architecture shall satisfy the following goals.

- Lightweight
- Offline capable
- Simple installation
- Easy maintenance
- Future scalability

Version 1.0 targets laboratory desktop deployment.

---

# 3. High-Level Deployment

```text
┌─────────────────────────────────────────────┐
│                 Desktop PC                  │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │          PyWebView Desktop UI        │   │
│  └──────────────────────────────────────┘   │
│                    │                        │
│                    ▼                        │
│  ┌──────────────────────────────────────┐   │
│  │          Flask Application           │   │
│  └──────────────────────────────────────┘   │
│                    │                        │
│                    ▼                        │
│  ┌──────────────────────────────────────┐   │
│  │        Planning & Scheduling         │   │
│  └──────────────────────────────────────┘   │
│                    │                        │
│                    ▼                        │
│  ┌──────────────────────────────────────┐   │
│  │             SQLite DB                │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

All components execute on the same workstation.

---

# 4. Runtime Components

The application consists of five runtime components.

Presentation

PyWebView

Business

Planning Engine

Optimization

Scheduling Engine

Persistence

SQLite

Infrastructure

Logging

Each component may evolve independently.

---

# 5. Deployment Modes

Version 1.0 supports Desktop Mode.

```text
Desktop

↓

SQLite

↓

Single User
```

Future versions may support:

- Shared PostgreSQL
- Web Deployment
- Multi-user Deployment

No Domain changes shall be required.

---

# 6. Configuration Files

Runtime configuration shall be externalized.

Suggested files:

```text
config.yaml

logging.yaml

solver.yaml
```

Configuration files shall never contain business data.

---

# 7. Database Strategy

Development

SQLite

Production (Future)

PostgreSQL

Database migration shall be handled through Alembic.

---

# 8. Logging

Application logs shall be separated into:

Application Log

Scheduling Log

Audit Log

Unexpected exceptions shall always be logged.

---

# 9. Backup Strategy

The following data shall be backed up.

- SQLite Database
- Configuration Files
- Exported Plans

Temporary Scheduling Models shall not be backed up.

---

# 10. Future Deployment

The architecture supports future deployment without changing business code.

Examples:

Desktop

↓

Docker

↓

Linux Server

↓

Cloud

The Deployment Layer may evolve independently from the Planning Domain.

---

# 11. Architectural Rules

1. Deployment never changes business logic.

2. Configuration remains external.

3. Database technology is replaceable.

4. The Planning Domain is deployment-independent.

5. OR-Tools remains an internal implementation detail.

6. Desktop deployment is the baseline for Version 1.0.
