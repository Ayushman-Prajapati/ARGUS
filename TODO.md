# ARGUS — CURRENT SPRINT

Status

🚧 Active Development

Current Version

**v0.3.0**

Current Phase

**Phase 3.5 — Design Refresh**

Current Branch

`feature/design-refresh`

---

# Sprint Goal

Establish the **Midnight Slate** design system that will define ARGUS's visual identity.

This sprint focuses **only** on the global design system.

Objectives

- Create reusable design tokens
- Establish the new color palette
- Improve typography
- Standardize spacing
- Standardize borders
- Standardize shadows
- Preserve all existing functionality

No backend changes.

No database changes.

No scanner changes.

No authentication changes.

No architecture changes.

---

# Sprint Rules

One sprint at a time.

Each completed sprint must be

- Implemented
- Reviewed
- Tested
- Committed
- Verified

One prompt = One sprint = One commit.

---

# Sprint 1 — Design System Foundation

Status

⬜ Pending

Objectives

- CSS Design Tokens
- Midnight Slate Color Palette
- Typography
- Border Radius
- Shadows
- Focus States
- Transition Tokens

Primary Files

- static/css/custom.css

Optional

- templates/base.html (fonts only)

---

# Sprint 2 — Navigation

Status

⬜ Pending

Objectives

- Navbar
- Sidebar
- Active Navigation
- Hover States

---

# Sprint 3 — Core Components

Status

⬜ Pending

Objectives

- Cards
- Buttons
- Badges
- Alerts
- Progress Bars

---

# Sprint 4 — Forms & Tables

Status

⬜ Pending

Objectives

- Inputs
- Selects
- Textareas
- Tables
- Pagination
- Filters

---

# Sprint 5 — Dashboard Polish

Status

⬜ Pending

Objectives

- Dashboard Cards
- Analytics
- Charts
- Quick Actions
- Activity Timeline

No layout redesign.

---

# Sprint 6 — Scan Detail Polish

Status

⬜ Pending

Objectives

- Findings
- Code Viewer
- Severity Badges
- Metadata
- Executive Summary

---

# Sprint 7 — Reports

Status

⬜ Pending

Objectives

- Report Layout
- Typography
- Tables
- Charts
- PDF Styling

---

# Sprint 8 — Accessibility & Final Polish

Status

⬜ Pending

Objectives

- Keyboard Navigation
- Contrast Improvements
- Responsive Review
- Animation Cleanup
- Cross-browser Validation

---

# Out of Scope

Do NOT modify

- AST Engine
- Bandit Integration
- Semgrep Integration
- Safety Integration
- pip-audit Integration
- Scanner Services
- Authentication
- REST API
- Docker
- Repository Explorer
- AI Features

Unless explicitly requested.

---

# Verification Checklist

Every completed sprint must satisfy

☐ Django starts successfully

☐ No Python errors

☐ Existing scans still work

☐ Existing reports still work

☐ Existing dashboard functionality preserved

☐ Responsive layout maintained

☐ Charts continue rendering

☐ Accessibility preserved

☐ No backend regressions

☐ No CSS regressions

☐ Design tokens reused

---

# Commit Strategy

One sprint = One commit

Examples

style(ui): establish Midnight Slate design tokens

style(ui): refresh navigation

style(ui): modernize core components

style(ui): improve forms and tables

style(ui): polish dashboard

style(ui): refine scan detail

style(ui): refresh reports

style(ui): finalize design system

Never combine multiple unrelated sprints into one commit.

---

# Claude Instructions

Before editing

1. Inspect the existing implementation.
2. Explain the implementation strategy.
3. List every file that will be modified.
4. Wait for approval if more than two files require modification.

After editing

1. Verify Django starts successfully.
2. Verify existing functionality.
3. Verify responsive layout.
4. Verify accessibility.
5. Verify no backend regressions.
6. Stop.

Never automatically continue to the next sprint.

Wait for the next prompt.