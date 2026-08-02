# ARGUS ROADMAP

Version: 5.0

Status: Active Development

---

# Vision

ARGUS is a modular Secure Code Review Platform built with Django.

Its long-term goal is to become a production-ready Application Security (AppSec) platform capable of helping developers continuously discover, understand, prioritize, and remediate security vulnerabilities.

The platform will evolve incrementally while maintaining:

- Security
- Clean Architecture
- Modular Design
- Extensibility
- Performance
- Maintainability
- Professional User Experience

---

# Current Status

Current Version

**v0.3.0**

Current Phase

**Phase 3.5 — Design Refresh**

Current Branch

`feature/design-refresh`

---

# Development Strategy

ARGUS follows feature-driven development.

Every feature:

- Lives on its own Git feature branch
- Is independently testable
- Preserves backward compatibility
- Includes documentation updates
- Is completed before the next major feature begins

Every phase represents a significant milestone.

---

# Completed Milestones

## Phase 1 — Scan Detail Experience

Status

✅ Completed

Highlights

- Professional Scan Detail page
- Executive Summary
- Risk Score
- Code Viewer
- Charts
- Responsive Design
- Accessibility improvements

---

## Phase 2 — Dashboard & Security

Status

✅ Completed

Highlights

- Security Dashboard
- Dashboard Analytics
- Recent Scans
- Activity Timeline
- Highest Risk Projects
- Quick Actions
- Authentication
- User Data Isolation
- Protected Reports

---

## Phase 3 — Modular AST Engine

Status

✅ Completed

Highlights

Architecture

- Modular AST Engine
- Rule Registry
- Base Rule
- Rule Discovery
- Finding Normalization

Implemented Rules

- Dangerous Functions
- Command Injection
- SQL Injection
- Unsafe Deserialization
- Hardcoded Secrets
- Weak Cryptography

Additional Work

- Unit Tests
- Documentation
- Cleanup
- Performance Improvements

---

# Phase 3.5 — Design Refresh

Status

🚧 In Progress

Objective

Modernize the visual identity of ARGUS while preserving the existing architecture.

Goals

- Midnight Slate design system
- Design tokens
- Typography improvements
- Enterprise color palette
- Component consistency
- Accessibility improvements
- Responsive refinement

This phase introduces no backend architecture changes.

---

# Phase 4 — Dedicated Secret Scanner

Status

📅 Planned

Features

- Entropy Analysis
- Regex Detection
- Ignore Rules
- Custom Patterns
- File Type Support
- Secret Classification

---

# Phase 5 — Dependency Scanner

Status

📅 Planned

Support

- requirements.txt
- Pipfile.lock
- poetry.lock
- package.json
- Cargo.toml
- composer.json

Future

- OSV
- CVE Database
- CVSS
- License Analysis
- Upgrade Recommendations

---

# Phase 6 — Repository Explorer

Status

📅 Planned

Features

- Repository Tree
- File Preview
- Syntax Highlighting
- Search
- Breadcrumb Navigation
- Jump to Finding
- Repository Metadata

---

# Phase 7 — AI Security Assistant

Status

📅 Planned

Features

- Vulnerability Explanation
- Attack Scenarios
- Secure Code Suggestions
- CWE Guidance
- OWASP Guidance
- Risk Prioritization

---

# Phase 8 — Reporting

Status

📅 Planned

Export Formats

- PDF
- HTML
- SARIF
- JSON
- CSV

Reporting

- Executive Summary
- Risk Metrics
- Findings
- Charts
- CWE Mapping
- OWASP Mapping
- Evidence
- Remediation

---

# Phase 9 — Background Processing

Status

📅 Planned

Technology

- Celery
- Redis

Features

- Scan Queue
- Live Progress
- Retry
- Cancellation
- Worker Monitoring

---

# Phase 10 — REST API

Status

📅 Planned

Modules

- Projects
- Scans
- Findings
- Reports
- Dashboard

Features

- Authentication
- Filtering
- Pagination
- OpenAPI
- Swagger UI

---

# Phase 11 — Enterprise Features

Status

📅 Planned

Features

- Organizations
- Teams
- Projects
- RBAC
- SSO
- GitHub Login
- Google Login
- Microsoft Login

---

# Phase 12 — Production Deployment

Status

📅 Planned

Infrastructure

- Docker
- Docker Compose
- PostgreSQL
- Gunicorn
- Nginx
- GitHub Actions
- CI/CD
- Monitoring
- Structured Logging

---

# Future Integrations

Source Control

- GitHub
- GitLab
- Bitbucket
- Azure DevOps

Developer Tools

- VS Code Extension
- CLI
- Desktop Client

CI/CD

- GitHub Actions
- GitLab CI
- Jenkins

---

# Long-Term Vision

ARGUS should become a modern Application Security platform that enables developers and security teams to continuously improve software security throughout the software development lifecycle.

The project should always prioritize:

- Security
- Accuracy
- Scalability
- Performance
- Developer Experience
- Maintainability

---

# Definition of Done

A phase is complete only when:

- ✅ Django starts successfully
- ✅ No Python errors
- ✅ No template regressions
- ✅ No JavaScript regressions
- ✅ No CSS regressions
- ✅ Existing functionality preserved
- ✅ Tests pass
- ✅ Feature merged into `main`
- ✅ Documentation updated
- ✅ Version tag created