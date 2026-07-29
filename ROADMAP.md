# ARGUS ROADMAP

Version: 4.0

Status: Active Development

---

# Vision

ARGUS is a modular Secure Code Review Platform built with Django.

Its long-term objective is to become a production-ready Application Security (AppSec) platform capable of performing:

- Static Application Security Testing (SAST)
- Secret Detection
- Dependency Analysis
- Repository Exploration
- AI-assisted Security Explanations
- Professional Security Reporting

The platform should evolve incrementally while maintaining:

- Clean Architecture
- Modular Design
- Security
- Performance
- Extensibility
- Professional User Experience

---

# Current Status

Current Version

**v0.2.0**

Current Phase

**Phase 3 — Custom AST Engine**

Current Development Branch

`feature/ast-engine`

---

# Development Strategy

Development is feature-driven.

Each feature:

- Lives on its own Git feature branch
- Is independently testable
- Is fully documented
- Preserves existing functionality
- Is completed before another major feature begins

Every phase represents a major milestone.

---

# Phase 1 — Scan Detail Experience

Status

✅ Completed

Deliverables

- Executive Summary
- Metadata Grid
- Findings
- Filters
- Risk Score
- Code Viewer
- Charts
- Responsive Layout
- Accessibility
- UI Cleanup

---

# Phase 2 — Dashboard & User Isolation

Status

✅ Completed

Deliverables

- Dashboard
- Analytics
- Activity Timeline
- Recent Scans
- Highest Risk Projects
- Quick Actions
- Responsive Design
- Empty States
- Authentication
- User Data Isolation
- Report Authorization

Security Improvements

- Per-user scan ownership
- Protected reports
- User-scoped dashboards
- Broken Access Control mitigation

---

# Phase 3 — Custom AST Engine

Status

🚧 In Progress

Objective

Build ARGUS's own modular static analysis framework.

---

## Sprint 1 — Engine Architecture

- AST Engine
- Rule Registry
- Base Rule
- Rule Discovery
- Finding Generator
- Engine Integration

---

## Sprint 2 — Dangerous Functions

Detect

- eval()
- exec()
- compile()
- input() misuse
- globals()
- locals()

---

## Sprint 3 — Command Injection

Detect

- os.system()
- os.popen()
- subprocess.run(shell=True)
- subprocess.Popen(shell=True)
- subprocess.call(shell=True)

---

## Sprint 4 — SQL Injection

Detect

- f-strings
- string concatenation
- .format()
- %-formatting
- execute() misuse

---

## Sprint 5 — Unsafe Deserialization

Detect

- pickle.loads()
- marshal.loads()
- yaml.load()
- dill.loads()

---

## Sprint 6 — Secret Detection

Detect

- Hardcoded Passwords
- API Keys
- JWT Secrets
- AWS Keys
- GitHub Tokens
- Environment Secrets

---

## Sprint 7 — Weak Cryptography

Detect

- MD5
- SHA1
- DES
- ECB Mode
- Weak Random
- Predictable Tokens

---

## Sprint 8 — Optimization

- Performance
- Caching
- Parallel Rule Execution
- Documentation
- Test Suite

---

# Phase 4 — Secret Scanner

Status

📅 Planned

Features

- Entropy Analysis
- Regex Engine
- Custom Rules
- Ignore Lists
- User-defined Patterns

---

# Phase 5 — Dependency Scanner

Status

📅 Planned

Support

- requirements.txt
- poetry.lock
- Pipfile.lock
- package.json
- Cargo.toml
- composer.json

Future

- OSV
- CVE Database
- CVSS
- License Analysis
- Upgrade Suggestions

---

# Phase 6 — Repository Explorer

Status

📅 Planned

Features

- Folder Tree
- File Preview
- Syntax Highlighting
- Breadcrumbs
- Search
- Jump to Finding
- File Metadata

---

# Phase 7 — AI Security Assistant

Status

📅 Planned

Features

- Vulnerability Explanation
- Attack Scenario
- Remediation
- Secure Code Example
- CWE Explanation
- OWASP Explanation
- AI Risk Prioritization

---

# Phase 8 — Reporting

Status

📅 Planned

Exports

- PDF
- HTML
- SARIF
- JSON
- CSV

Include

- Executive Summary
- Risk Score
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
- Progress Tracking
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
- Swagger
- OpenAPI

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

Technology

- Docker
- Docker Compose
- PostgreSQL
- Gunicorn
- Nginx

Infrastructure

- Environment Variables
- Logging
- GitHub Actions
- CI/CD
- Monitoring

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

# Long-Term Goal

ARGUS should become a complete Application Security platform capable of helping developers discover, understand, prioritize, and remediate security vulnerabilities throughout the software development lifecycle.

The project should always prioritize:

- Security
- Accuracy
- Performance
- Scalability
- Developer Experience
- Maintainability

---

# Definition of Done

A sprint is complete only when:

- ✅ Django starts successfully
- ✅ No Python errors
- ✅ No template regressions
- ✅ No JavaScript regressions
- ✅ No CSS regressions
- ✅ Existing functionality preserved
- ✅ Tests pass
- ✅ Feature committed
- ✅ Merged into `main`
- ✅ Documentation updated