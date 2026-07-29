# ARGUS

## Secure Code Review Platform

---

# Overview

ARGUS is a modular Secure Code Review Platform built with Django that helps developers and security teams identify vulnerabilities through automated static analysis.

The platform analyzes source code using multiple security engines, aggregates findings into a unified format, calculates project risk, and generates professional security reports.

ARGUS is designed with extensibility in mind, allowing new security scanners and analysis engines to be integrated without major architectural changes.

The long-term vision is to evolve ARGUS into a production-ready Application Security (AppSec) platform.

---

# Inspiration

ARGUS is inspired by industry-leading security platforms including:

- GitHub Advanced Security
- SonarQube
- Snyk
- Semgrep

The goal is **not** to copy these platforms, but to adopt the architectural principles that make them scalable, maintainable, and effective.

---

# Development Status

Current Version

**v0.2.0**

Current Phase

**Phase 3 — Custom AST Engine**

Current Objective

Build ARGUS's own extensible Python static analysis engine capable of detecting security vulnerabilities beyond third-party scanners.

---

# Core Features

## Authentication & Authorization

- Secure user authentication
- Per-user project isolation
- Protected scan reports
- User-specific dashboards
- Broken Access Control mitigation

---

## Scan Methods

Supported scan sources:

- Upload Python File
- Upload ZIP Project
- Paste Python Code
- Scan GitHub Repository

---

## Security Analysis Engines

### Bandit

Python security linter for common security vulnerabilities.

### Semgrep

Rule-based static analysis engine supporting multiple programming languages.

### Safety

Dependency vulnerability analysis.

### pip-audit

Python package vulnerability auditing.

### ARGUS AST Engine (In Development)

A custom Python Abstract Syntax Tree (AST) analysis engine developed specifically for ARGUS.

The AST engine is intended to become the platform's primary differentiating feature.

---

# Existing Functionality

The following modules are considered stable:

## Dashboard

- Security Overview
- Dashboard Analytics
- Severity Distribution
- Engine Distribution
- Activity Timeline
- Recent Scans
- Highest Risk Projects
- Quick Actions

---

## Scan Management

- Scan History
- Scan Detail
- Risk Score
- Executive Summary
- Findings
- Code Viewer
- Severity Filters
- Engine Filters
- Re-scan Support

---

## Reporting

- PDF Report Generation
- Executive Summary
- Vulnerability Details
- Risk Metrics

---

# Architecture

ARGUS follows a modular architecture.

```
argus_platform/

accounts/
authentication/

scanner/
    models.py
    views.py
    forms.py
    services.py

    scanners/
        bandit/
        semgrep/
        safety/
        pip_audit/
        ast_engine/

    templates/
    templatetags/

reports/

templates/

static/

PROMPTS/

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

Future

- PostgreSQL

---

# Design Philosophy

ARGUS follows a professional cybersecurity design language.

Characteristics:

- Dark Theme
- Professional
- Modern
- Responsive
- Minimal
- Information Dense
- Accessible

The interface should prioritize usability over visual effects.

---

# Engineering Principles

The project emphasizes:

- Clean Architecture
- Modularity
- Extensibility
- Security
- Maintainability
- Performance
- Reusability

Prefer:

- Small incremental improvements
- Independent modules
- Reusable components
- Service-oriented design

Avoid:

- Large rewrites
- Tight coupling
- Duplicate logic
- Breaking existing functionality

---

# Current Development Focus

Phase 3 focuses exclusively on the custom AST engine.

Planned milestones:

### Sprint 1

- AST Architecture
- Rule Registry
- Base Rule
- Engine Integration

### Sprint 2

- Dangerous Function Detection

### Sprint 3

- Command Injection Detection

### Sprint 4

- SQL Injection Detection

### Sprint 5

- Unsafe Deserialization

### Sprint 6

- Secret Detection

### Sprint 7

- Weak Cryptography Detection

### Sprint 8

- Performance Optimization
- Testing
- Documentation

No UI redesigns should occur during this phase unless required for integration.

---

# Long-Term Roadmap

## Static Analysis

- Bandit
- Semgrep
- Safety
- pip-audit
- ARGUS AST Engine

## Security Scanners

- Secret Scanning
- Dependency Scanning
- License Scanning
- Configuration Scanning

## Repository Features

- Repository Explorer
- GitHub Integration
- Multi-language Support

## Reporting

- PDF Reports
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
- Projects
- RBAC
- Scan Scheduling
- Notifications
- REST API
- Docker Deployment
- CI/CD Integration
- Background Workers

Every new feature should integrate naturally into the existing architecture without requiring major refactoring.