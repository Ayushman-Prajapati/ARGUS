# ARGUS

## Secure Code Review Platform

---

# Vision

ARGUS is a modular Secure Code Review Platform built with Django that helps developers and security teams identify, understand, and remediate security vulnerabilities through automated static analysis.

The platform combines multiple security engines into a unified workflow, producing consistent findings, project risk scores, and professional security reports.

ARGUS is designed with extensibility as a core principle, allowing new analysis engines, scanners, and integrations to be added with minimal architectural changes.

The long-term vision is to evolve ARGUS into a production-ready Application Security (AppSec) platform.

---

# Inspiration

ARGUS draws architectural inspiration from:

- GitHub Advanced Security
- SonarQube
- Snyk
- Semgrep

The objective is **not** to replicate these platforms, but to adopt the engineering principles that make them scalable, maintainable, and developer-friendly.

---

# Current Status

Current Version

**v0.3.0**

Current Phase

**Phase 3.5 — Design Refresh**

Current Objective

Modernize ARGUS's visual design system while preserving the stable backend architecture developed during previous phases.

---

# Platform Modules

## Authentication

- Secure authentication
- User isolation
- Protected scan reports
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

Integrated analysis engines

- Bandit
- Semgrep
- Safety
- pip-audit
- ARGUS AST Engine

The modular AST Engine is ARGUS's primary differentiating feature and provides native security rule execution through an extensible rule framework.

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
- Filtering
- Re-scan Support

---

## Reporting

- Executive Summary
- PDF Reports
- Risk Metrics
- Vulnerability Details

---

# Architecture

```
argus_platform/

accounts/
authentication/

scanner/
├── models.py
├── views.py
├── forms.py
├── services.py
├── engines/
│   ├── bandit_engine.py
│   ├── semgrep_engine.py
│   ├── ast_engine.py
│   └── ast/
│       ├── registry.py
│       ├── base_rule.py
│       ├── findings.py
│       ├── utils.py
│       └── rules/
├── templates/
└── templatetags/

reports/

templates/

static/

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

ARGUS follows the **Midnight Slate** design system.

Characteristics

- Professional
- Enterprise
- Modern
- Minimal
- Calm
- Information Dense
- Accessible

The interface should emphasize readability, consistency, and usability over visual effects.

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
- Reusable components
- Low coupling
- High cohesion
- Service-oriented architecture

Avoid

- Large rewrites
- Duplicate logic
- Tight coupling
- Breaking changes
- Premature optimization

---

# Current Development

Current focus

**Phase 3.5 — Design Refresh**

Objectives

- Establish the Midnight Slate design system
- Modernize the user interface
- Improve visual consistency
- Improve accessibility
- Preserve all existing functionality

No backend architecture changes are planned during this phase.

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

## Reporting

- HTML Reports
- SARIF Export
- CSV Export
- JSON Export

## AI Features

- AI Vulnerability Explanations
- AI Remediation Suggestions
- Secure Coding Recommendations
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

ARGUS aims to become a modular, production-ready Application Security platform that enables developers and security teams to continuously identify, prioritize, and remediate security vulnerabilities while maintaining a clean, scalable, and maintainable architecture.