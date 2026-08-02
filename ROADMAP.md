# ARGUS ROADMAP

Version: 6.0

Status: Active Development

---

# Vision

ARGUS is a modular Secure Code Review Platform built with Django.

Its long-term objective is to become a production-ready Application Security (AppSec) platform capable of helping developers continuously discover, understand, prioritize, and remediate security vulnerabilities throughout the software development lifecycle.

The platform evolves incrementally while maintaining:

- Security
- Clean Architecture
- Modularity
- Extensibility
- Performance
- Maintainability
- Professional User Experience

---

# Current Status

Current Version

**v0.4.0**

Current Phase

**Phase 5 — Scan Experience**

Current Branch

`feature/scan-experience`

---

# Development Strategy

ARGUS follows feature-driven development.

Every feature:

- Lives on its own Git feature branch
- Is independently testable
- Preserves existing functionality
- Includes documentation updates
- Is completed before the next major feature begins

Every phase represents a major milestone.

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
- Accessibility Improvements

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
- User Isolation
- Protected Reports

---

## Phase 3 — ARGUS AST Engine

Status

✅ Completed

Highlights

Architecture

- Modular AST Engine
- Rule Registry
- Base Rule
- Rule Framework
- Finding Normalization

Implemented Rules

- Dangerous Functions
- Command Injection
- SQL Injection
- Unsafe Deserialization
- Hardcoded Secret Detection
- Weak Cryptography

Additional Work

- Unit Tests
- Documentation
- Cleanup
- Performance Improvements

---

## Phase 4 — Design System Refresh

Status

✅ Completed

Highlights

- Amber Terminal Design System
- Global Design Tokens
- IBM Plex Typography
- Enterprise UI Refresh
- Consistent Component Styling
- Improved Charts
- PDF Theme Alignment
- Accessibility Improvements

---

# Phase 5 — Scan Experience

Status

🚧 In Progress

Objective

Transform scanning into a modern, interactive workflow that provides continuous feedback instead of static loading screens.

Planned Sprints

### Sprint 1

- Live Scan Progress
- Progress Bar
- Progress States

### Sprint 2

- Engine-by-Engine Progress
- Individual Engine Status
- Progress Indicators

### Sprint 3

- Scan Lifecycle Improvements
- Better Running States
- Success / Failure Handling

### Sprint 4

- Re-scan Improvements
- Updated Scan Date
- Improved Scan History
- Duplicate Prevention

### Sprint 5

- Interactive Demo Scan
- Simulated Progress
- Better Demo Experience

### Sprint 6

- Live Scan Console
- Scan Logs
- Engine Output

### Sprint 7

- Notifications
- Toast Messages
- Better User Feedback

### Sprint 8

- Scan Comparison
- Risk Delta
- Findings Comparison

---

# Phase 6 — Dedicated Secret Scanner

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

# Phase 7 — Dependency Scanner

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

- OSV Integration
- CVE Database
- CVSS Scoring
- License Analysis
- Upgrade Recommendations

---

# Phase 8 — Repository Explorer

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

# Phase 9 — AI Security Assistant

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

# Phase 10 — Reporting

Status

📅 Planned

Exports

- PDF
- HTML
- SARIF
- JSON
- CSV

Features

- Executive Summary
- Risk Metrics
- Findings
- Charts
- CWE Mapping
- OWASP Mapping
- Evidence
- Remediation

---

# Phase 11 — Background Processing

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

# Phase 12 — REST API

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
- Swagger

---

# Phase 13 — Enterprise Features

Status

📅 Planned

Features

- Organizations
- Teams
- RBAC
- SSO
- GitHub Login
- Google Login
- Microsoft Login

---

# Phase 14 — Production Deployment

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

ARGUS aims to become a modern Application Security platform that enables developers and security teams to continuously identify, prioritize, and remediate security vulnerabilities through automated analysis, professional reporting, and an exceptional developer experience.

The project will always prioritize:

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