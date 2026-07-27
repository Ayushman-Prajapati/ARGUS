# Sprint 4 — Quick Actions

## Objective

Improve the Dashboard by creating a professional Quick Actions section that gives users fast access to common tasks.

This sprint focuses ONLY on the Quick Actions section.

Do not redesign the Dashboard Hero.

Do not modify Recent Scans.

Do not modify Dashboard Analytics.

Do not modify backend logic.

Do not modify Django views, models, URLs, forms, or context variables.

---

# Before Writing Code

1. Inspect the existing Dashboard implementation.
2. Explain the planned modifications.
3. List every file that will be modified.
4. If more than two files require modification, stop and wait for confirmation.

---

# Scope

Improve only the Quick Actions section.

Do not modify any other dashboard components.

---

# Requirements

Create a clean and modern Quick Actions panel.

The section should provide one-click access to the most common tasks within Argus.

Reuse existing routes and URLs.

Do not introduce new backend functionality.

---

## Quick Action Cards

Create responsive action cards for:

- Start New Scan
- Upload Project
- Scan GitHub Repository
- View Reports
- Settings

Only display actions that already exist within the application.

Do not create placeholder URLs.

---

## Card Design

Each action card should include:

- Icon
- Title
- Short description
- Hover effect
- Clickable card/button

Cards should have:

- Rounded corners
- Soft shadow
- Equal height
- Consistent spacing

---

## Layout

Requirements

- Responsive grid
- Equal-width cards
- Proper spacing
- Balanced alignment
- Compact layout

Avoid oversized whitespace.

---

## Hover Effects

Cards should have subtle interactions such as:

- Slight elevation
- Border highlight
- Shadow enhancement
- Smooth transition

Animations should remain subtle and professional.

---

## Accessibility

Ensure:

- Keyboard accessible
- Visible focus states
- Proper button semantics
- Accessible labels where appropriate

---

## Responsive Design

Verify on:

- Desktop
- Tablet
- Mobile

Cards should wrap naturally without breaking the layout.

---

## CSS Rules

Use:

static/css/custom.css

Requirements:

- Reuse existing variables
- Reuse utility classes
- Avoid duplicate CSS
- Avoid inline styles
- Preserve Argus design language

---

## HTML Rules

Reuse the existing Dashboard template.

Improve only the Quick Actions section.

Do not replace the page.

Do not remove existing components.

---

# Out of Scope

Do NOT modify:

- Dashboard Hero
- Recent Scans
- Analytics
- Activity Timeline
- Empty State
- Scan Detail
- Reports
- Authentication
- Backend logic
- Database
- JavaScript logic

These belong to future sprints.

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
- Existing navigation works
- Existing functionality preserved
- No CSS regressions
- No unnecessary whitespace

---

# Stop Condition

After completing Quick Actions:

- Stop immediately.
- Do not begin Activity Timeline.
- Do not begin Empty State.
- Do not begin Cleanup.
- Do not perform unrelated improvements.

Wait for the next prompt before continuing.