# ARGUS ROADMAP

Version: 3.1

Status: Active Development

---

# Vision

Argus is a modern Secure Code Review Platform built with Django.

Its long-term goal is to become an enterprise-grade Application Security (AppSec) platform capable of performing:

- Static Application Security Testing (SAST)
- Secret Detection
- Dependency Analysis
- Repository Exploration
- AI-assisted Security Explanations
- Professional Reporting

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

- Lives on its own Git feature branch
- Is independently testable
- Preserves existing functionality
- Is completed before beginning the next major feature

Each phase represents a significant milestone in the evolution of Argus.

---

# Phase 1 — Scan Detail Experience

Status

✅ Completed

Completed Sprints

- Executive Summary
- Metadata Grid
- Findings Section
- Findings Filters
- Risk Score Card
- Code Viewer
- Charts
- Responsive Design
- Final Cleanup

Deliverables

- Professional Scan Detail page
- Modern cybersecurity UI
- Responsive layout
- Improved usability
- Maintainable frontend

---

# Phase 2 — Dashboard

Status

🚧 In Progress

Current Sprint Progress

- ✅ Dashboard Hero
- ✅ Recent Scans
- ✅ Dashboard Analytics
- ✅ Quick Actions
- ✅ Activity Timeline
- 🔄 Highest Risk Projects
- ⏳ Responsive & Empty States
- ⏳ Final Cleanup & Accessibility

Objectives

Build a professional security operations dashboard.

Core Components

- Dashboard Hero
- Security Overview Cards
- Dashboard Analytics
- Recent Scans
- Quick Actions
- Activity Timeline
- Highest Risk Projects
- Responsive Layout
- Empty States
- Accessibility Improvements

Future Enhancements

- Risk Trends
- Historical Analytics
- Scan Velocity
- Team Activity
- Project Health Metrics

Success Criteria

- Responsive on all devices
- Fast rendering
- Consistent design language
- Professional AppSec appearance
- Matches Scan Detail quality

---

# Phase 3 — Static Analysis Engine

Status

📅 Planned

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

Future

- Rule engine
- Plugin architecture
- Custom detection rules

---

# Phase 4 — Secret Scanner

Status

📅 Planned

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
- User-defined Secret Patterns

---

# Phase 5 — Dependency Scanner

Status

📅 Planned

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

Status

📅 Planned

Objectives

Build a VS Code–style repository browser.

Features

- Folder Tree
- File Preview
- Syntax Highlighting
- Search Files
- Jump to Vulnerability
- File Metadata
- Breadcrumb Navigation

---

# Phase 7 — AI Security Assistant

Status

📅 Planned

Objectives

Provide AI-assisted vulnerability explanations.

Each finding should include

- Why it is vulnerable
- Attack scenario
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

# Phase 8 — Reports

Status

📅 Planned

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

Export Formats

- PDF
- HTML
- SARIF
- JSON
- CSV

---

# Phase 9 — Background Processing

Status

📅 Planned

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

Status

📅 Planned

Objectives

Expose platform functionality through REST APIs.

Modules

- Projects API
- Findings API
- Reports API
- Dashboard API

Features

- Authentication
- Pagination
- Filtering
- Swagger UI
- OpenAPI Specification

---

# Phase 11 — Authentication & Organizations

Status

📅 Planned

Objectives

Support enterprise collaboration.

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
- Single Sign-On (SSO)

---

# Phase 12 — DevOps & Deployment

Status

📅 Planned

Objectives

Production-ready deployment.

Technology

- Docker
- Docker Compose
- PostgreSQL
- Gunicorn
- Nginx

Infrastructure

- Environment Variables
- Structured Logging
- Production Settings
- GitHub Actions
- CI/CD Pipeline

---

# Future Integrations

## Source Control

- GitHub
- GitLab
- Bitbucket
- Azure DevOps

## Developer Tools

- VS Code Extension
- Command Line Interface (CLI)
- Desktop Client

## CI/CD

- Jenkins
- GitHub Actions
- GitLab CI

---

# Long-Term Vision

Argus should evolve into a complete Application Security platform capable of helping developers identify, understand, prioritize, and remediate security vulnerabilities throughout the software development lifecycle.

The emphasis should always remain on:

- Accuracy
- Performance
- Scalability
- Developer Experience
- Professional User Interface

---

# Coding Principles

Always prefer

- Small incremental improvements
- Clean architecture
- Modular components
- Readable code
- Reusable code
- Stable functionality
- Professional UI consistency

Avoid

- Large rewrites
- Breaking existing functionality
- Duplicate code
- Premature optimization
- Unnecessary complexity

---

# Definition of Done

A feature is complete only when:

- ✅ Application starts successfully
- ✅ No Python errors
- ✅ No template errors
- ✅ No CSS regressions
- ✅ No JavaScript regressions
- ✅ Responsive on desktop, tablet, and mobile
- ✅ Existing functionality preserved
- ✅ Code reviewed
- ✅ Committed to its feature branch
- ✅ Merged into `main`
- ✅ Documentation updated