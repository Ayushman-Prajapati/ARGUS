# ARGUS

## Project Overview

Argus is a Secure Code Review Platform built with Django.

Its primary objective is to analyze source code, identify security vulnerabilities, and generate actionable security reports using multiple static analysis engines.

Argus is designed as a modular Application Security (AppSec) platform capable of growing into a production-ready secure code analysis solution.

The platform is inspired by:

- GitHub Advanced Security
- SonarQube
- Snyk
- Semgrep

The project emphasizes:

- Clean Architecture
- Modularity
- Maintainability
- Extensibility
- Professional UI/UX
- Secure Development Practices

---

# Current Development Phase

## Phase 2 — Dashboard

Current focus:

Design and implement a modern security dashboard that provides users with an overview of their application security posture.

Current dashboard objectives include:

- Security overview
- Recent scans
- Statistics & analytics
- Quick actions
- Activity timeline
- Responsive layout
- Empty state experience

Only the Dashboard should be modified during this phase unless explicitly requested.

---

# Current Features

## Scan Methods

Supported scan methods:

- Upload Python File
- Upload ZIP Project
- Paste Python Code
- Scan GitHub Repository

---

## Security Engines

### Bandit

Python security linter for detecting common security vulnerabilities.

### Semgrep

Rule-based static analysis engine supporting multiple programming languages.

### ARGUS AST Engine

Custom Python Abstract Syntax Tree (AST) analyzer for project-specific security checks.

---

# Existing Functionality

The following functionality already exists and should remain stable:

- Dashboard
- Scan History
- Scan Detail
- Risk Score
- Executive Summary
- Findings List
- Severity Filters
- Engine Filters
- Code Viewer
- Severity Charts
- Engine Charts
- PDF Report Generation
- Re-scan Support
- Remediation Suggestions

Unless explicitly requested, these features must not be redesigned or broken.

---

# Project Structure

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
    templatetags/
    templates/

reports/

templates/
    scanner/

static/
    css/
    js/
    images/

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

Argus follows a modern cybersecurity design system.

Characteristics:

- Dark Theme
- Cyber Security Aesthetic
- Professional
- Minimal
- Glassmorphism (subtle)
- Rounded Cards
- Soft Shadows
- Responsive Layout
- Consistent Spacing
- Compact Scrolling

Pages should be improved incrementally.

Entire page redesigns should be avoided.

---

# Development Philosophy

Argus follows a feature-driven development workflow.

Each feature should be:

- Independently developed
- Incrementally improved
- Fully tested
- Completed before beginning another major feature

Avoid:

- Large rewrites
- Breaking existing functionality
- Unrelated refactoring
- Duplicate code

Prefer:

- Small improvements
- Reusable components
- Modular architecture
- Maintainable code

---

# Stability Requirements

The following components should remain compatible unless explicitly modified:

- URLs
- Views
- Models
- Forms
- Context Variables
- Reports
- PDF Generation
- Charts
- Filters
- Pagination
- Navigation
- Bootstrap Responsiveness

---

# UI Principles

Argus should resemble a professional enterprise security platform.

The interface should prioritize:

- Readability
- Usability
- Consistency
- Accessibility
- Performance

Visual effects should support the user experience without becoming distracting.

Animations should remain subtle.

Whitespace should be intentional.

Layouts should remain compact and information-dense.

---

# Long-Term Roadmap

Argus will gradually evolve into a complete Secure Code Review Platform with:

## Static Analysis

- Bandit
- Semgrep
- AST Engine

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
- CSV / JSON Export

## AI Features

- AI Vulnerability Explanation
- AI Remediation Suggestions
- Secure Code Recommendations
- Risk Prioritization

## Platform Features

- Authentication
- Organizations
- Projects
- Scan Scheduling
- Notifications
- REST API
- Docker Deployment
- CI/CD Integration
- Background Workers
- Role-Based Access Control (RBAC)

Every future feature should integrate naturally into the existing architecture.

Avoid shortcuts that make future expansion difficult.