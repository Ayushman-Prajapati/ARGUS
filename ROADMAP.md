# ARGUS ROADMAP

Version: 3.0

Status: Active Development

---

# Vision

Argus is a modern Secure Code Review Platform built with Django.

Its long-term goal is to provide enterprise-grade static application security testing (SAST), secret detection, dependency analysis, repository exploration, AI-assisted remediation, and professional reporting.

The platform should evolve incrementally while maintaining:

- Clean Architecture
- Modular Design
- Professional UI/UX
- Stable Functionality
- Maintainable Code

---

# Development Strategy

Development is feature-driven.

Every feature:

- Is implemented on its own Git branch
- Is independently testable
- Must not break existing functionality
- Is completed before starting the next major feature

Each phase represents a major milestone.

---

# Phase 1 — Scan Detail Experience

Status

✅ Completed

Objectives

- Executive Summary
- Metadata Grid
- Findings Section
- Findings Filters
- Risk Score Card
- Code Viewer
- Charts
- Responsive Design
- Cleanup

Deliverables

- Professional Scan Detail page
- Responsive layout
- Modern cybersecurity UI
- Improved usability

---

# Phase 2 — Dashboard

Status

🚧 In Progress

Objectives

Build a professional security dashboard.

Components

- Dashboard Hero
- Security Overview
- Statistics Cards
- Recent Scans
- Security Analytics
- Quick Actions
- Activity Timeline
- Empty States
- Responsive Design

Future

- Risk Trends
- Historical Analytics
- Scan Metrics
- Team Activity

Success Criteria

- Responsive
- Fast
- Clean layout
- Consistent with Scan Detail

---

# Phase 3 — Static Analysis Engine

Objectives

Expand the ARGUS AST Engine.

Detect

- eval()
- exec()
- os.system()
- subprocess(shell=True)
- pickle.loads()
- yaml.load()
- weak hashing
- insecure randomness
- DEBUG=True
- hardcoded secrets
- SQL Injection
- Command Injection
- Path Traversal
- Unsafe Deserialization

Each finding should include

- Severity
- Confidence
- CWE
- OWASP
- Description
- Evidence
- Remediation
- References

---

# Phase 4 — Secret Scanner

Objectives

Create a dedicated Secret Detection Engine.

Detect

- AWS Keys
- Azure Keys
- GCP Keys
- GitHub Tokens
- GitLab Tokens
- Slack Tokens
- Discord Tokens
- JWT Tokens
- RSA Keys
- SSH Keys
- OpenAI Keys
- Anthropic Keys
- Gemini Keys
- Stripe Keys
- Twilio Keys
- Hardcoded Passwords

Future

- Entropy Analysis
- Custom Regex Rules
- User-defined Patterns

---

# Phase 5 — Dependency Scanner

Objectives

Support

- requirements.txt
- poetry.lock
- Pipfile.lock
- package.json
- Cargo.toml
- composer.json

Future

- OSV Integration
- CVE Database
- CVSS Scoring
- Upgrade Recommendations
- License Detection

---

# Phase 6 — Repository Explorer

Objectives

Build a VS Code–style repository browser.

Features

- Folder Tree
- File Preview
- Syntax Highlighting
- Search Files
- Jump to Vulnerability
- File Metadata

---

# Phase 7 — Reports

Objectives

Professional reporting.

Include

- Executive Summary
- Findings
- Charts
- Risk Score
- CWE Mapping
- OWASP Mapping
- Evidence
- Remediation
- Appendix

Exports

- PDF
- HTML
- SARIF
- JSON
- CSV

---

# Phase 8 — AI Security Assistant

Objectives

Provide AI-assisted vulnerability explanations.

Each finding should include

- Why it is vulnerable
- Possible attack scenario
- Secure alternative
- OWASP explanation
- CWE explanation
- Secure code example

Future

- LLM Integration
- Offline Explanations
- AI Risk Prioritization
- AI Secure Refactoring

---

# Phase 9 — Background Processing

Objectives

Introduce asynchronous scanning.

Technology

- Celery
- Redis

Features

- Scan Queue
- Progress Tracking
- Live Updates
- Cancellation
- Retry
- Worker Monitoring

---

# Phase 10 — REST API

Objectives

Expose platform functionality through APIs.

Modules

- Projects API
- Findings API
- Reports API
- Dashboard API

Features

- Authentication
- Pagination
- Filtering
- Swagger
- OpenAPI

---

# Phase 11 — Authentication & Organizations

Objectives

Support multi-user collaboration.

Features

- Authentication
- Organizations
- Projects
- Teams
- Roles
- Permissions

Roles

- Administrator
- Member
- Viewer

Future

- GitHub Login
- Google Login
- Microsoft Login
- SSO

---

# Phase 12 — DevOps & Deployment

Objectives

Production deployment.

Technology

- Docker
- Docker Compose
- PostgreSQL
- Gunicorn
- Nginx

Infrastructure

- Environment Variables
- Logging
- Production Settings
- GitHub Actions
- CI/CD

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

- Jenkins
- GitHub Actions
- GitLab CI

---

# Coding Principles

Always prefer

- Small incremental improvements
- Modular architecture
- Readable code
- Reusable components
- Clean UI
- Stable functionality

Avoid

- Large rewrites
- Breaking changes
- Duplicate code
- Premature optimization

---

# Definition of Done

A feature is complete only when:

- ✅ Application starts successfully
- ✅ No Python errors
- ✅ No template errors
- ✅ No CSS regressions
- ✅ Responsive on desktop, tablet, and mobile
- ✅ Existing functionality preserved
- ✅ Code reviewed
- ✅ Committed to feature branch
- ✅ Merged into `main`
- ✅ Documentation updated