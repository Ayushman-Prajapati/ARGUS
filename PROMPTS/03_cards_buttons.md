# Phase 4 — Sprint 3

## Cards & Reusable Components

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Modernize ARGUS's reusable UI components using the established **Midnight Slate** design system.

This sprint focuses on reusable interface components only.

The goal is to create a consistent, professional enterprise appearance across the application while preserving all existing functionality.

Do not redesign pages.

Do not modify layouts.

---

# Background

The following have already been completed:

- Midnight Slate Design System
- Navigation Refresh

This sprint applies those design tokens to reusable components used throughout ARGUS.

---

# Scope

Refresh the appearance of:

- Cards
- Buttons
- Badges
- Alerts
- Progress Bars
- Status Indicators
- Empty States
- Loading States (if present)

All components should consume the design tokens introduced in Sprint 1.

---

# Cards

Improve

- Background
- Borders
- Shadows
- Border radius
- Internal spacing
- Headers
- Footers

Cards should rely primarily on borders for separation.

Shadows should remain subtle.

Avoid heavy elevation.

---

# Buttons

Refresh all button variants.

Primary

- Midnight Slate blue accent

Secondary

- Outlined style

Danger

- Muted red

Success

- Green

Warning

- Amber

Improve

- Hover states
- Active states
- Disabled states
- Focus states

Do not introduce gradients.

---

# Badges

Refresh badges including severity indicators.

Severity colors

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

Badges should remain compact and highly readable.

---

# Alerts

Improve

- Success alerts
- Warning alerts
- Danger alerts
- Information alerts

Use subtle backgrounds with strong readable text.

Avoid bright solid fills.

---

# Progress Bars

Improve

- Height
- Border radius
- Colors
- Background track

Maintain existing behavior.

---

# Empty States

Improve visual presentation for pages with no data.

Examples

- No scans
- No reports
- No findings

Improve

- Typography
- Spacing
- Icons (if already present)
- Visual hierarchy

Do not add illustrations.

---

# Loading States

If loading indicators exist

Improve

- Spinner colors
- Progress indicators
- Skeleton styles (if present)

Do not introduce new loading systems.

---

# Design Rules

Use only the Midnight Slate design tokens.

Avoid

- Gradients
- Glow effects
- Glassmorphism
- Neon colors
- Large shadows

Prefer

- Soft borders
- Consistent spacing
- Clean typography
- Subtle animations

---

# Accessibility

Ensure

- Buttons maintain sufficient contrast.
- Disabled states remain distinguishable.
- Focus indicators remain visible.
- Status colors are not the only indicator of meaning.

---

# Do NOT

Do NOT modify

- Django views
- URLs
- Authentication
- Dashboard layout
- Scan Detail layout
- Reports
- Backend logic
- JavaScript behavior

Do not redesign pages.

Do not move components.

---

# Files Allowed To Change

Primary

```
static/css/custom.css
```

If necessary

Shared templates containing reusable components.

Do not modify unrelated templates.

---

# Verification

Verify

✓ Cards render correctly

✓ Buttons remain functional

✓ Alerts display correctly

✓ Badges render correctly

✓ Progress bars function correctly

✓ Empty states remain responsive

✓ Existing functionality preserved

✓ Responsive layouts maintained

✓ Accessibility maintained

✓ Django starts successfully

---

# Deliverables

At the end of this sprint:

- Cards should have a modern enterprise appearance.
- Buttons should be visually consistent.
- Badges should clearly communicate severity.
- Alerts should match the Midnight Slate design language.
- Progress bars should integrate with the new design system.

No page layouts should change.

---

# Commit Message

```text
style(ui): modernize reusable components
```

---

# Stop

After verification

STOP.

Do not begin Forms & Tables improvements.

Wait for the next sprint.
```