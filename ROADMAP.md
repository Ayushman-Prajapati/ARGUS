# ARGUS ROADMAP

Version: 2.0
Status: In Development

---

# Vision

Argus will become a modern Secure Code Review Platform capable of analyzing source code, detecting vulnerabilities, explaining security risks, and producing professional reports.

The project should evolve gradually without sacrificing code quality.

---

# Development Strategy

Development follows incremental feature releases.

Every release must leave the application fully functional.

Each feature is developed on its own Git branch.

No feature should require redesigning the entire application.

---

# Phase 1
## Professional UI

Status:
IN PROGRESS

Objectives

- Improve Scan Detail page
- Improve Dashboard
- Improve Homepage
- Better typography
- Better spacing
- Better responsiveness
- Better findings cards
- Better charts
- Better code viewer

Success Criteria

- No layout regressions
- Mobile responsive
- Existing functionality preserved

---

# Phase 2
## Better Static Analysis

Objectives

Improve ARGUS AST Engine.

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
- Remediation
- References

---

# Phase 3
## Secret Detection

Objectives

Create a dedicated Secret Scanner.

Detect

- AWS Keys
- Azure Keys
- GCP Keys
- GitHub Tokens
- GitLab Tokens
- Slack Tokens
- Discord Tokens
- JWT
- RSA Keys
- SSH Keys
- OpenAI Keys
- Anthropic Keys
- Gemini Keys
- Stripe Keys
- Twilio Keys
- Passwords

Future

Entropy analysis

Custom regex rules

---

# Phase 4
## Dependency Scanning

Objectives

Support

requirements.txt

poetry.lock

Pipfile.lock

package.json

Cargo.toml

composer.json

Future

OSV integration

Package risk scoring

CVSS

Upgrade recommendations

---

# Phase 5
## Repository Explorer

Objectives

VSCode-style file explorer.

Features

- Folder tree
- File preview
- Syntax highlighting
- Jump to vulnerability
- Search files

---

# Phase 6
## AI Security Assistant

Objectives

Each finding should provide

Explain

Why vulnerable

Attack example

Secure alternative

OWASP explanation

CWE explanation

Secure code example

Future

LLM integration

Caching

Offline explanations

---

# Phase 7
## Reports

Objectives

Improve PDF reports.

Include

Executive Summary

Charts

Risk Score

OWASP Mapping

CWE

Evidence

Remediation

Appendix

Future

HTML Reports

SARIF Export

JSON Export

CSV Export

---

# Phase 8
## Dashboard

Objectives

Executive Dashboard

Recent Scans

Recent Findings

Risk Trends

Top Vulnerabilities

Most Vulnerable Projects

Engine Statistics

Future

Historical analytics

Trend charts

---

# Phase 9
## Background Processing

Objectives

Use

Celery

Redis

Queue

Progress tracking

Live updates

Cancellation

Retry

Worker monitoring

---

# Phase 10
## REST API

Objectives

Projects API

Findings API

Reports API

Dashboard API

Authentication

Pagination

Filtering

Swagger

OpenAPI

---

# Phase 11
## Authentication

Objectives

Organizations

Projects

Teams

Roles

Permissions

Admin

Member

Viewer

Future

SSO

GitHub Login

Google Login

---

# Phase 12
## DevOps

Objectives

Docker

Docker Compose

PostgreSQL

Gunicorn

Nginx

Environment Variables

Logging

Production Settings

CI/CD

GitHub Actions

---

# Future Integrations

GitHub

GitLab

Bitbucket

Azure DevOps

Jenkins

VS Code Extension

CLI

Desktop Client

---

# Coding Principles

Always prefer

Small improvements

Clean architecture

Modular code

Readable code

Reusable components

Avoid

Large rewrites

Breaking existing features

Duplicate code

Premature optimization

---

# Definition of Done

Every completed feature must satisfy

✓ Application starts successfully

✓ No template errors

✓ No Python errors

✓ No layout regressions

✓ Responsive

✓ Existing functionality preserved

✓ Code reviewed

✓ Committed to feature branch

✓ Ready for merge