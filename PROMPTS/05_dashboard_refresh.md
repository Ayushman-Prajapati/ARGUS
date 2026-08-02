# Phase 4 — Sprint 5

## Dashboard Refresh

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Modernize the Dashboard using the established **Midnight Slate** design system.

This sprint focuses exclusively on the Dashboard interface.

The goal is to improve hierarchy, readability, and visual consistency while preserving every existing feature and interaction.

Do not redesign the layout.

Do not modify backend logic.

---

# Background

The following have already been completed:

- Midnight Slate Design System
- Navigation Refresh
- Cards & Reusable Components
- Forms & Tables Refresh

This sprint applies the design system to the Dashboard only.

---

# Scope

Refresh the appearance of:

- Dashboard Header
- Statistics Cards
- Charts
- Quick Actions
- Recent Scans
- Highest Risk Projects
- Activity Timeline
- Empty States
- Dashboard Sections

Do not move components.

---

# Dashboard Header

Improve

- Page title
- Subtitle
- Spacing
- Alignment
- Visual hierarchy

The header should immediately communicate that ARGUS is an enterprise security platform.

---

# Statistics Cards

Improve

- Card appearance
- Typography
- Icons (if present)
- Value emphasis
- Supporting text
- Hover state

Maintain the current metrics and functionality.

---

# Charts

Improve the visual styling only.

Keep the existing Chart.js implementation.

Update

- Colors
- Grid lines
- Legends
- Tooltips
- Labels
- Backgrounds

Severity Palette

Critical

#E5484D

High

#FF8A3D

Medium

#FFB547

Low

#36C2FF

Info

#8895A7

Charts should match the Midnight Slate design system.

---

# Quick Actions

Improve

- Buttons
- Icons
- Spacing
- Hover feedback

Do not change available actions.

---

# Recent Scans

Improve

- Card styling
- Typography
- Status indicators
- Hover state
- Row spacing

Do not modify scan functionality.

---

# Highest Risk Projects

Improve

- Risk indicators
- Severity badges
- Spacing
- Typography

Maintain existing calculations.

---

# Activity Timeline

Improve

- Timeline spacing
- Timeline markers
- Typography
- Borders

Do not change the chronological ordering.

---

# Empty States

Improve presentation when no dashboard data exists.

Examples

- No scans
- No projects
- No recent activity

Improve

- Typography
- Spacing
- Visual hierarchy

Do not introduce illustrations or animations.

---

# Responsive Behavior

Verify

- Dashboard remains responsive.
- Charts resize correctly.
- Cards stack correctly.
- Mobile usability is preserved.

Do not redesign the responsive layout.

---

# Accessibility

Ensure

- Dashboard maintains WCAG-friendly contrast.
- Charts remain readable.
- Cards remain keyboard accessible.
- Interactive elements retain visible focus indicators.

---

# Design Rules

Use only the Midnight Slate design tokens.

Avoid

- Large gradients
- Heavy shadows
- Glassmorphism
- Neon colors

Prefer

- Clean spacing
- Soft borders
- Consistent typography
- Professional enterprise appearance

---

# Do NOT

Do NOT modify

- Django views
- Models
- URLs
- Scanner logic
- Reports
- Authentication
- Chart.js functionality
- Dashboard calculations

Do not move components.

Do not redesign the layout.

---

# Files Allowed To Change

Primary

```
static/css/custom.css
```

If necessary

```
templates/dashboard.html
templates/includes/*
```

Only if required for semantic improvements or styling hooks.

Do not modify backend files.

---

# Verification

Verify

✓ Dashboard renders correctly

✓ Statistics cards display correctly

✓ Charts continue functioning

✓ Quick Actions remain functional

✓ Recent Scans render correctly

✓ Highest Risk Projects render correctly

✓ Activity Timeline remains functional

✓ Empty states display correctly

✓ Responsive layout preserved

✓ Accessibility maintained

✓ Django starts successfully

---

# Deliverables

At the end of this sprint:

- Dashboard should feel modern and enterprise-grade.
- Statistics cards should clearly communicate key metrics.
- Charts should match the Midnight Slate design language.
- Dashboard sections should have improved hierarchy and spacing.
- Existing functionality should remain unchanged.

No backend behavior should change.

---

# Commit Message

```text
style(dashboard): refresh dashboard
```

---

# Stop

After verification

STOP.

Do not begin Scan Detail Refresh.

Wait for the next sprint.