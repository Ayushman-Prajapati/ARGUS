# Sprint 6 — Empty States

## Objective

Improve the Dashboard by creating professional Empty States for sections that have no available data.

This sprint focuses ONLY on Empty States.

Do not redesign existing Dashboard components.

Do not modify backend logic.

Do not modify Django views, models, URLs, forms, or context variables.

---

# Before Writing Code

1. Inspect the existing Dashboard implementation.
2. Identify every section that can display an empty state.
3. Explain the intended modifications.
4. List every file that will be modified.
5. If more than two files require modification, stop and wait for confirmation.

---

# Scope

Improve only Empty State user experience.

Do not modify existing Dashboard functionality.

---

# Requirements

Every Dashboard section that can have no data should display a clean, professional empty state instead of blank space.

Possible sections include:

- Dashboard Overview
- Recent Scans
- Analytics
- Activity Timeline

Only implement empty states where appropriate.

---

## Empty State Design

Each empty state should include:

- Appropriate Bootstrap Icon
- Clear heading
- Short descriptive message
- Primary Call-to-Action button (when applicable)

Examples

Recent Scans

"No scans found"

Start your first security scan to begin monitoring your projects.

Button

Start New Scan

---

Analytics

"No analytics available"

Charts will appear after completing your first scan.

---

Activity Timeline

"No recent activity"

Recent security events will appear here after scans are performed.

---

## Design Requirements

Maintain Argus design language.

Requirements

- Rounded cards
- Soft shadows
- Compact spacing
- Centered content
- Responsive layout
- Consistent typography

Avoid oversized whitespace.

---

## Icons

Use Bootstrap Icons only.

Examples

- bi-shield
- bi-search
- bi-graph-up
- bi-clock-history
- bi-folder

Do not introduce new icon libraries.

---

## Buttons

Reuse existing routes.

Do not create placeholder links.

Do not create fake functionality.

---

## Responsive Design

Verify:

- Desktop
- Tablet
- Mobile

Empty states should remain centered and visually balanced.

---

## CSS Rules

Use:

static/css/custom.css

Requirements:

- Reuse existing variables
- Reuse utility classes
- Avoid duplicate CSS
- Avoid inline styles
- Preserve dark cyber theme

---

## HTML Rules

Reuse existing Dashboard template.

Improve only Empty States.

Do not replace the page.

Do not remove existing components.

---

# Out of Scope

Do NOT modify:

- Dashboard Hero
- Recent Scans layout
- Analytics layout
- Quick Actions
- Activity Timeline layout
- Scan Detail
- Reports
- Authentication
- Backend logic
- Database
- JavaScript logic

These belong to other sprints.

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
- Existing functionality preserved
- No CSS regressions
- No broken navigation
- No unnecessary whitespace

---

# Stop Condition

After completing Empty States:

- Stop immediately.
- Do not begin Responsive Improvements.
- Do not begin Cleanup.
- Do not perform unrelated improvements.

Wait for the next prompt before continuing.