# ARGUS

## Secure Code Review Platform

---

# Vision

ARGUS is a modular Secure Code Review Platform built with Django that helps developers and security teams identify, understand, prioritize, and remediate security vulnerabilities through automated static analysis.

The platform combines multiple security analysis engines into a unified workflow, producing consistent findings, project risk scores, and professional security reports.

ARGUS is designed around clean architecture and extensibility, allowing new scanners, analysis engines, and integrations to be added with minimal changes to the existing codebase.

The long-term vision is to evolve ARGUS into a production-ready Application Security (AppSec) platform suitable for professional security teams.

---

# Inspiration

ARGUS takes engineering inspiration from industry-leading security platforms, including:

- GitHub Advanced Security
- SonarQube
- Snyk
- Semgrep

The objective is **not** to replicate these products, but to adopt the architectural and engineering principles that make them scalable, maintainable, and developer-friendly.

---

# Current Status

Current Version

**v0.4.0**

Current Phase

**Phase 5 — Scan Experience**

Current Objective

Improve the scan workflow by providing real-time progress feedback, a smoother scan lifecycle, enhanced re-scan behavior, and a more polished user experience while preserving the existing backend architecture.

---

# Platform Modules

## Authentication

- Secure authentication
- User isolation
- Protected reports
- User-specific dashboards
- Authorization enforcement

---

## Scan Sources

Supported scan methods

- Upload Python File
- Upload ZIP Project
- Paste Python Code
- Scan GitHub Repository

---

## Security Analysis

Integrated security engines

- Bandit
- Semgrep
- Safety
- pip-audit
- ARGUS AST Engine

The modular ARGUS AST Engine is the platform's primary differentiator, providing native rule-based security analysis through an extensible framework.

---

# Current Capabilities

## Dashboard

- Security Overview
- Analytics
- Severity Distribution
- Engine Distribution
- Activity Timeline
- Recent Scans
- Highest Risk Projects
- Quick Actions

---

## Scan Management

- Scan History
- Scan Details
- Executive Summary
- Risk Score
- Findings
- Code Viewer
- Severity Filters
- Engine Filters
- Re-scan Support

---

## Reporting

- Executive Summary
- Professional PDF Reports
- Risk Metrics
- Vulnerability Details
- Engine Breakdown
- Severity Charts

---

# Architecture

```
argus_platform/

accounts/
reports/
scanner/
│
├── engines/
│   ├── bandit_engine.py
│   ├── semgrep_engine.py
│   ├── ast_engine.py
│   └── ast/
│       ├── base_rule.py
│       ├── registry.py
│       ├── findings.py
│       ├── utils.py
│       └── rules/
│
├── services.py
├── views.py
├── forms.py
├── models.py
├── templates/
└── templatetags/

static/
templates/
PROMPTS/

README.md
PROJECT.md
ROADMAP.md
TODO.md
.claude.md
```

---

# Technology Stack

## Backend

- Django
- Python

## Frontend

- Bootstrap 5
- Chart.js
- Vanilla JavaScript

## Database

Current

- SQLite

Planned

- PostgreSQL

---

# Design Language

ARGUS uses the **Amber Terminal** design system.

Characteristics

- Professional
- Enterprise
- Minimal
- Terminal-inspired
- Accessible
- Information Dense
- High Contrast
- Monochromatic Identity

The interface emphasizes readability, consistency, and developer-focused usability over decorative visual effects.

---

# Engineering Principles

ARGUS emphasizes

- Security
- Clean Architecture
- Maintainability
- Extensibility
- Modularity
- Performance
- Reusability

Prefer

- Incremental development
- Reusable services
- Low coupling
- High cohesion
- Clear separation of concerns

Avoid

- Large rewrites
- Duplicate logic
- Tight coupling
- Breaking changes
- Premature optimization

---

# Current Development

Current focus

**Phase 5 — Scan Experience**

Objectives

- Live scan progress
- Engine-by-engine status
- Improved scan lifecycle
- Better re-scan workflow
- Interactive demo scan
- User notifications
- Scan history improvements

No major architectural redesigns are planned during this phase.

---

# Future Modules

## Static Analysis

- Multi-language support
- Additional AST rules
- Plugin architecture

## Security Scanners

- Dedicated Secret Scanner
- Dependency Scanner
- License Scanner
- Configuration Scanner

## Repository Features

- Repository Explorer
- GitHub Integration
- GitLab Integration
- Bitbucket Integration

## Reporting

- HTML Reports
- SARIF Export
- CSV Export
- JSON Export

## AI Features

- AI Vulnerability Explanations
- AI Remediation Suggestions
- Secure Code Examples
- Risk Prioritization

## Enterprise Features

- Organizations
- Teams
- RBAC
- Scan Scheduling
- REST API
- Docker Deployment
- CI/CD Integration
- Background Workers

---

# Long-Term Goal

ARGUS aims to become a modular, enterprise-grade Application Security platform that enables developers and security teams to continuously identify, prioritize, and remediate security vulnerabilities through automated analysis, professional reporting, and an intuitive user experience.

Every new feature should strengthen the platform while preserving clean architecture, maintainability, and scalability.