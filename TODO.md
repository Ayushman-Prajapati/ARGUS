# ARGUS - CURRENT SPRINT

Status

🚧 Active Development

Current Phase

Phase 2 — Dashboard

Current Branch

feature/dashboard

---

# Sprint Goal

Design and implement a modern Dashboard that provides users with an overview of their application security posture.

This sprint focuses ONLY on the Dashboard.

No backend architecture changes.

No database changes.

No authentication work.

No scan engine work.

No report generation work.

---

# Sprint Rules

One feature at a time.

Each completed feature must be

- Implemented
- Tested
- Reviewed
- Committed

before starting the next feature.

---

# Sprint Checklist

## Dashboard Hero

Status

⬜ Pending

Requirements

- Welcome heading
- Dashboard subtitle
- "Start New Scan" button
- Clean hero section
- Responsive layout

Files

templates/scanner/dashboard.html

static/css/custom.css

---

## Security Overview Cards

Status

⬜ Pending

Requirements

Display

- Total Scans
- Total Findings
- Critical Findings
- Average Risk Score

Improve

- Typography
- Card layout
- Icons
- Hover effects

No backend changes.

---

## Recent Scans

Status

⬜ Pending

Requirements

Display

- Repository
- Scan Date
- Status
- Risk Score
- Findings Count
- View Report button

Improve table responsiveness.

Do not modify backend variables.

---

## Dashboard Analytics

Status

⬜ Pending

Requirements

Improve analytics section.

Include

- Severity Distribution
- Scan Trend
- Engine Usage

Reuse existing Chart.js implementation.

No backend changes.

---

## Quick Actions

Status

⬜ Pending

Requirements

Create action cards for

- New Scan
- Upload Project
- GitHub Scan
- Reports
- Settings

Responsive layout.

No backend changes.

---

## Activity Timeline

Status

⬜ Pending

Requirements

Display recent events

- Scan Started
- Scan Completed
- Critical Finding
- Report Exported

Newest events first.

Responsive design.

---

## Empty State

Status

⬜ Pending

Requirements

Professional empty state.

Include

- Helpful message
- Illustration or icon
- Call-to-action button

Avoid excessive whitespace.

---

## Mobile Responsiveness

Status

⬜ Pending

Requirements

Verify

- Desktop
- Tablet
- Mobile

No layout regressions.

---

## Cleanup

Status

⬜ Pending

Requirements

- Remove duplicate CSS
- Remove inline styles
- Improve spacing
- Improve accessibility
- Remove unnecessary wrappers

No functionality changes.

---

# Out of Scope

Do NOT work on

- Scan Detail
- Homepage
- Reports
- Authentication
- REST API
- Docker
- Repository Explorer
- Secret Scanner
- Dependency Scanner
- AST Engine
- AI Explanations

These belong to future phases.

---

# Testing Checklist

Every completed feature must satisfy

☐ Django starts successfully

☐ No template errors

☐ No Python errors

☐ No console errors

☐ Charts render correctly

☐ Buttons work

☐ Existing navigation works

☐ Responsive layout

☐ No excessive scrolling

☐ No unnecessary whitespace

☐ Existing functionality preserved

---

# Commit Strategy

One feature = One commit

Examples

feat(dashboard): add dashboard hero

feat(dashboard): add security overview cards

feat(dashboard): improve recent scans

feat(dashboard): add analytics section

feat(dashboard): implement quick actions

feat(dashboard): add activity timeline

feat(dashboard): improve responsive layout

Never combine multiple unrelated features into one commit.

---

# Claude Instructions

Before editing

1. Inspect the existing implementation.
2. Explain the intended changes.
3. List every file that will be modified.
4. Wait if changes affect more than two files.

After editing

1. Verify Django runs successfully.
2. Verify the dashboard layout.
3. Verify responsiveness.
4. Verify existing functionality.
5. Stop.

Never continue to another feature automatically.