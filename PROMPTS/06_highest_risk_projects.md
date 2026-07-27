# Sprint 6 — Highest Risk Projects

## Objective

Improve the existing "Highest Risk Projects" section to match the quality and design language of the rest of the Dashboard.

This sprint focuses ONLY on the Highest Risk Projects section.

Do not redesign the Dashboard.

Do not modify backend logic.

Do not modify Django views, models, URLs, forms, or context variables.

---

# Before Writing Code

1. Inspect the existing Highest Risk Projects implementation.
2. Explain the intended improvements.
3. List every file that will be modified.
4. If more than two files require modification, stop and wait for confirmation.

---

# Scope

Improve only the Highest Risk Projects section.

Do not modify:

- Dashboard Hero
- Overview Cards
- Analytics
- Quick Actions
- Activity Timeline
- Recent Scans

---

# Requirements

Modernize the Highest Risk Projects table while preserving all existing functionality.

Reuse existing backend data.

Do not introduce new template variables.

---

## Table Columns

Display existing information such as:

- Project Name
- Risk Score
- Findings
- Last Scanned
- View Report

Use existing backend variables only.

---

## Risk Score

Improve presentation.

Examples

- Color-coded score
- Inline progress indicator
- Severity badge
- Risk level label

Reuse existing dashboard colors.

Do not modify backend calculations.

---

## Findings

Improve visibility.

Examples

- Monospace count
- Severity-aware color
- Compact badge

Do not introduce new calculations.

---

## Project Information

Improve readability.

Requirements

- Better typography
- Truncated long names
- Optional repository icon (if data already exists)
- Consistent spacing

---

## Action Button

Improve the existing View button.

Allow subtle polish such as:

- Better hover effect
- Icon
- Rounded corners
- Consistent sizing

Do not change URLs.

---

## Table Design

Requirements

- Compact layout
- Responsive
- Row hover effect
- Consistent spacing
- Sticky header (optional)
- Rounded container

Avoid oversized whitespace.

---

## Empty State

If no projects exist:

Display

- Friendly icon
- Helpful message
- Call-to-action button

Reuse existing Dashboard design language.

---

## Responsive Design

Verify

- Desktop
- Tablet
- Mobile

Maintain readability.

Avoid horizontal scrolling where possible.

---

## CSS Rules

Use

static/css/custom.css

Requirements

- Reuse existing variables
- Reuse utility classes
- Avoid duplicate CSS
- Avoid inline styles
- Preserve Argus design language

---

## HTML Rules

Reuse the existing Dashboard template.

Improve only the Highest Risk Projects section.

Do not replace the page.

Do not remove working functionality.

---

# Out of Scope

Do NOT modify

- Dashboard Hero
- Analytics
- Quick Actions
- Activity Timeline
- Recent Scans
- Authentication
- Reports
- Backend logic
- Database
- JavaScript

These belong to other sprints.

---

# Files Expected

Expected files

- templates/scanner/dashboard.html
- static/css/custom.css

No other files should be modified unless absolutely necessary.

---

# Verification

After implementation, verify

✓ Django starts successfully

✓ No template errors

✓ No Python errors

✓ Responsive layout

✓ Existing dashboard functionality preserved

✓ No CSS regressions

✓ No broken navigation

✓ No unnecessary whitespace

---

# Stop Condition

After completing Highest Risk Projects

- Stop immediately.
- Do not begin Responsive improvements.
- Do not begin Cleanup.
- Do not modify unrelated sections.

Wait for the next prompt.