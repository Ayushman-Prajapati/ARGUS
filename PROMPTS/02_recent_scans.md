# Sprint 2 — Recent Scans

## Objective

Improve the existing "Recent Scans" section of the Dashboard.

This sprint focuses ONLY on the Recent Scans component.

Do not redesign the Dashboard Hero.

Do not modify backend logic.

Do not modify Django views, models, URLs, forms, or context variables.

---

# Before Writing Code

1. Inspect the existing Recent Scans implementation.
2. Explain the intended improvements.
3. List every file that will be modified.
4. If more than two files require modification, stop and wait for confirmation.

---

# Scope

Improve only the Recent Scans section.

Do not modify any other dashboard components.

---

# Requirements

Create a professional Recent Scans table that is clean, compact, and easy to scan.

Use existing backend data only.

Do not introduce new template variables.

---

## Table Columns

Display existing information such as:

- Repository / Project Name
- Scan Date
- Status
- Risk Score
- Findings Count
- Scan Engine (if available)
- View Report action

Use existing data already passed to the template.

---

## Status Badges

Improve the visual appearance of scan status.

Example statuses:

- Completed
- Running
- Failed
- Queued

Use Bootstrap badge styles or existing utility classes.

---

## Risk Score

Improve presentation.

Examples:

- Color-coded badge
- Progress indicator
- Risk level label

Do not modify backend calculations.

---

## Table Design

Requirements

- Responsive
- Compact
- Professional spacing
- Sticky header (optional if already supported)
- Hover effect
- Rounded container
- Consistent typography

Avoid excessive whitespace.

---

## Empty State

If no scans exist, display:

- Friendly icon
- Helpful message
- "Start New Scan" button

Reuse existing styling.

---

## Responsive Design

Verify layout on:

- Desktop
- Tablet
- Mobile

On smaller screens:

- Prevent horizontal overflow where possible
- Maintain readability
- Stack or collapse content only if necessary

---

## CSS Rules

Use:

static/css/custom.css

Requirements:

- Reuse existing variables
- Reuse existing utility classes
- Avoid duplicate CSS
- Avoid inline styles
- Preserve dark cyber theme

---

## HTML Rules

Reuse the existing Dashboard template.

Do not replace the page.

Improve only the Recent Scans section.

Do not remove working components.

---

# Out of Scope

Do NOT modify:

- Dashboard Hero
- Analytics Charts
- Quick Actions
- Activity Timeline
- Empty State (outside this section)
- Scan Detail
- Reports
- Authentication
- Backend logic
- Database
- JavaScript

These belong to later sprints.

---

# Files Expected

Expected files:

- templates/scanner/dashboard.html
- static/css/custom.css

No other files should be modified unless absolutely necessary.

---

# Verification

After implementation, verify:

- Django runs successfully
- No template errors
- No Python errors
- Responsive layout
- Existing dashboard functionality preserved
- No CSS regressions
- No broken navigation
- No unnecessary whitespace

---

# Stop Condition

After completing the Recent Scans section:

- Stop immediately.
- Do not begin Dashboard Analytics.
- Do not begin Quick Actions.
- Do not begin Activity Timeline.
- Do not perform unrelated cleanup.

Wait for the next prompt before continuing.