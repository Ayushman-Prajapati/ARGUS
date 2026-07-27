# Sprint 5 — Activity Timeline

## Objective

Improve the Dashboard by creating a professional Activity Timeline that displays recent security-related events.

This sprint focuses ONLY on the Activity Timeline.

Do not redesign the Dashboard Hero.

Do not modify Recent Scans.

Do not modify Dashboard Analytics.

Do not modify Quick Actions.

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

Improve only the Activity Timeline section.

Do not modify any other Dashboard components.

---

# Requirements

Create a professional Activity Timeline showing the most recent security events.

Use only existing data.

Do not introduce new backend variables.

---

## Timeline Events

Display existing events when available, such as:

- Scan Started
- Scan Completed
- Scan Failed
- Critical Vulnerability Detected
- Report Generated
- Repository Scanned

If event types are unavailable, gracefully display the existing activity data.

---

## Timeline Item Design

Each timeline item should include:

- Event icon
- Event title
- Short description
- Timestamp
- Status indicator (if available)

Maintain a clean vertical timeline layout.

---

## Visual Design

Requirements

- Vertical timeline
- Connecting line
- Circular event indicators
- Equal spacing
- Compact layout
- Rounded container
- Consistent typography

Avoid oversized whitespace.

---

## Icons

Use appropriate Bootstrap Icons (or existing icon library).

Examples:

- Shield
- Check Circle
- Warning Triangle
- Clock
- File
- Git Branch

Do not introduce additional icon libraries.

---

## Empty State

If no activity exists, display:

- Friendly icon
- Informative message
- Encourage the user to perform their first scan

Do not leave blank space.

---

## Responsive Design

Verify:

- Desktop
- Tablet
- Mobile

Timeline should remain readable without horizontal scrolling.

---

## CSS Rules

Use:

static/css/custom.css

Requirements:

- Reuse existing variables
- Reuse utility classes
- Avoid duplicate CSS
- Avoid inline styles
- Preserve the existing Argus design language

---

## HTML Rules

Reuse the existing Dashboard template.

Improve only the Activity Timeline section.

Do not replace the page.

Do not remove existing components.

---

# Out of Scope

Do NOT modify:

- Dashboard Hero
- Recent Scans
- Dashboard Analytics
- Quick Actions
- Empty State (outside the timeline)
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
- Existing dashboard functionality preserved
- No CSS regressions
- No broken navigation
- No unnecessary whitespace

---

# Stop Condition

After completing the Activity Timeline:

- Stop immediately.
- Do not begin Empty States.
- Do not begin Responsive Cleanup.
- Do not begin Final Cleanup.
- Do not perform unrelated improvements.

Wait for the next prompt before continuing.