# Sprint 1 — Dashboard Hero

## Objective

Improve the existing Dashboard by building a professional hero section and security overview.

This task focuses ONLY on the Dashboard Hero.

Do not redesign the entire page.

Do not modify backend logic.

Do not modify Django views, models, URLs, forms, or context variables.

---

# Before Writing Code

1. Inspect the existing dashboard implementation.
2. Explain the planned modifications.
3. List every file that will be modified.
4. If more than two files require modification, stop and wait for confirmation.

---

# Scope

Improve only the top section of the Dashboard.

The hero should immediately communicate the user's security posture.

---

# Requirements

Create a modern Dashboard Hero containing:

## Welcome Section

Display:

- Welcome heading (e.g., "Security Dashboard")
- Short descriptive subtitle
- Professional spacing
- Responsive layout

---

## Primary Action

Create a prominent action button.

Button:

- Start New Scan

Use the existing Bootstrap styling where possible.

Do not change existing URLs or functionality.

---

## Security Overview Cards

Design four responsive summary cards.

Cards should display existing dashboard values (do not create new backend variables).

Cards:

- Total Scans
- Total Findings
- Critical Findings
- Average Risk Score

Each card should include:

- Icon
- Large metric
- Label
- Small supporting text (if available)

---

## Card Design

Cards should follow the existing Argus design language.

Requirements:

- Rounded corners
- Soft shadow
- Subtle hover animation
- Consistent spacing
- Equal heights
- Responsive grid

Do not introduce excessive whitespace.

---

## Responsiveness

Verify layout for:

- Desktop
- Tablet
- Mobile

Cards should stack naturally on smaller screens.

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

Improve only the Hero section.

Do not remove existing components.

---

## Out of Scope

Do NOT modify:

- Recent Scans
- Charts
- Activity Timeline
- Quick Actions
- Empty State
- Scan Detail
- Reports
- Authentication
- Backend logic
- Database
- JavaScript

These will be handled in later sprints.

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

After completing the Dashboard Hero:

- Stop immediately.
- Do not begin Recent Scans.
- Do not begin Charts.
- Do not begin Quick Actions.
- Do not perform unrelated cleanup.

Wait for the next prompt before continuing.