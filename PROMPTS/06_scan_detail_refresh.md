# Phase 4 — Sprint 6

## Scan Detail Refresh

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Modernize the Scan Detail experience using the established **Midnight Slate** design system.

This sprint focuses exclusively on the Scan Detail page.

The goal is to improve readability, information hierarchy, and the overall user experience while preserving every existing feature and interaction.

Do not redesign the page.

Do not modify backend logic.

---

# Background

The following have already been completed:

- Midnight Slate Design System
- Navigation Refresh
- Cards & Reusable Components
- Forms & Tables Refresh
- Dashboard Refresh

This sprint applies the design system to the Scan Detail experience.

---

# Scope

Refresh the appearance of:

- Page Header
- Executive Summary
- Risk Score
- Metadata Section
- Findings List
- Finding Cards
- Severity Badges
- Code Viewer
- Filters
- Empty States

Preserve the current layout and functionality.

---

# Page Header

Improve

- Scan title
- Project name
- Metadata alignment
- Visual hierarchy
- Spacing

The header should immediately communicate the scan context without feeling cluttered.

---

# Executive Summary

Improve

- Card styling
- Typography
- Supporting text
- Section spacing
- Readability

Do not change the generated content.

---

# Risk Score

Improve

- Visual emphasis
- Typography
- Progress indicators (if present)
- Supporting information

Maintain the existing risk calculations.

---

# Metadata Section

Improve

- Labels
- Values
- Grid spacing
- Borders
- Alignment

Metadata should be easy to scan without overwhelming the user.

---

# Findings

Improve

- Finding cards
- Finding spacing
- Borders
- Hover states
- Severity emphasis
- Titles
- Description readability

Preserve finding order.

Do not modify finding data.

---

# Severity Badges

Refresh severity badges using the established palette.

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

Badges should remain compact and immediately recognizable.

---

# Code Viewer

Improve

- Background
- Borders
- Typography
- Syntax readability
- Padding
- Scrollbars
- Line spacing

Do not replace the existing syntax highlighting implementation.

---

# Filters

Improve

- Severity filters
- Engine filters
- Search controls
- Active states

Maintain all existing filtering behavior.

---

# Empty States

Improve presentation when:

- No findings exist
- Filters return no results
- Code snippets are unavailable

Improve

- Typography
- Spacing
- Visual hierarchy

Do not introduce illustrations.

---

# Responsive Behavior

Verify

- Findings remain readable.
- Code viewer remains usable.
- Metadata adapts correctly.
- Cards stack appropriately.
- Mobile experience remains functional.

Do not redesign the responsive layout.

---

# Accessibility

Ensure

- Keyboard navigation works.
- Code viewer remains readable.
- Focus indicators remain visible.
- Severity is not communicated by color alone.
- Contrast remains WCAG-friendly.

---

# Design Rules

Use only the Midnight Slate design tokens.

Avoid

- Heavy shadows
- Neon colors
- Gradients
- Glassmorphism
- Decorative animations

Prefer

- Clean spacing
- Soft borders
- Professional typography
- Consistent visual hierarchy

---

# Do NOT

Do NOT modify

- Django views
- Models
- URLs
- Scanner logic
- Report generation
- Authentication
- Finding calculations
- Risk calculations

Do not move components.

Do not redesign the page layout.

---

# Files Allowed To Change

Primary

```
static/css/custom.css
```

If necessary

```
templates/scanner/scan_detail.html
templates/scanner/includes/*
```

Only if required for semantic improvements or styling hooks.

Do not modify backend files.

---

# Verification

Verify

✓ Scan Detail renders correctly

✓ Executive Summary displays correctly

✓ Risk Score displays correctly

✓ Findings render correctly

✓ Severity badges display correctly

✓ Code Viewer remains functional

✓ Filters continue working

✓ Empty states render correctly

✓ Responsive layout preserved

✓ Accessibility maintained

✓ Django starts successfully

---

# Deliverables

At the end of this sprint:

- Scan Detail should have a modern enterprise appearance.
- Findings should be easier to read.
- Metadata should have improved hierarchy.
- Code Viewer should feel polished and professional.
- Existing functionality should remain unchanged.

No backend behavior should change.

---

# Commit Message

```text
style(scan-detail): modernize scan detail
```

---

# Stop

After verification

STOP.

Do not begin Reports Refresh.

Wait for the next sprint.
```