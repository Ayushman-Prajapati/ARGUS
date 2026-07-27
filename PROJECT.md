# ARGUS

## Overview

Argus is a Secure Code Review Platform built using Django.

The goal is to analyze uploaded source code and detect security vulnerabilities using multiple scanning engines.

Argus is designed to evolve into a professional Application Security (AppSec) platform inspired by:

- GitHub Advanced Security
- SonarQube
- Snyk
- Semgrep

The emphasis is on clean architecture, modularity, maintainability, and professional UI/UX.

---

# Current Features

## Scan Methods

- Upload Python file
- Upload ZIP project
- Paste Python code
- Scan GitHub repository

---

## Scan Engines

### Bandit

Python security linter.

Detects common Python security issues.

---

### Semgrep

Rule-based static analysis.

Supports multiple languages.

---

### ARGUS AST Engine

Custom Python AST scanner.

Detects project-specific security issues.

---

# Existing Functionality

Current application includes

- Dashboard
- Scan history
- Scan detail page
- Risk score
- Severity charts
- Engine charts
- PDF reports
- Re-scan
- Severity filters
- Engine filters
- Findings list
- Code snippets
- Remediation suggestions

These features must remain functional unless explicitly modified.

---

# Project Structure

scanner/
    models.py
    views.py
    forms.py
    services.py
    scanners/
    templates/

reports/
    PDF generation

templates/
    scanner/

static/
    css/
    js/
    images/

accounts/
    authentication

---

# Current Design Language

Theme

Dark

Cyber Security

Professional

Minimal

Modern

Rounded cards

Soft shadows

Subtle animations

Responsive

Do not redesign the entire application.

Improve incrementally.

---

# Technology Stack

Backend

- Django

Frontend

- Bootstrap 5
- Chart.js
- Vanilla JavaScript

Database

- SQLite (development)

Future

- PostgreSQL

---

# Development Philosophy

The project is feature-driven.

Every feature should be developed independently.

Avoid large rewrites.

Avoid breaking existing functionality.

Each feature should be completed before starting another.

---

# What Should Never Break

- Existing URLs
- Existing forms
- Existing views
- Existing models
- Existing reports
- Existing PDF generation
- Existing filters
- Existing charts
- Existing navigation
- Existing Bootstrap responsiveness

---

# Design Goals

Argus should feel like a professional security product.

The interface should emphasize:

- readability
- usability
- speed
- consistency

rather than visual complexity.

Animations should be subtle.

Whitespace should be intentional.

Cards should align consistently.

Scrolling should remain compact.

---

# Long-Term Vision

Argus will evolve into a complete Secure Code Review Platform with:

- SAST
- Secret Scanning
- Dependency Scanning
- Repository Explorer
- AI Explanations
- Risk Analytics
- REST API
- Authentication
- Organizations
- Docker Deployment
- CI/CD Integration

Every future feature should fit naturally into the existing architecture.

Avoid shortcuts that make future expansion difficult.