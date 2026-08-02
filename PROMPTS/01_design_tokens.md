# Phase 4 — Sprint 1

## Midnight Slate Design System

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Establish the new global design system for ARGUS.

This sprint introduces the **Midnight Slate** visual identity that will serve as the foundation for every future UI improvement.

The goal is to replace the current generic dark Bootstrap appearance with a professional enterprise security platform aesthetic while preserving every existing page and interaction.

This sprint creates the foundation only.

Do not redesign components or pages.

---

# Background

ARGUS already contains:

- Dashboard
- Scan Detail
- Reports
- Authentication
- Navigation
- Bootstrap components
- Responsive layouts

These already function correctly.

Only the global design language should change.

---

# Design Language

Theme

**Midnight Slate**

Characteristics

- Professional
- Enterprise
- Calm
- Minimal
- Information Dense
- Modern
- Developer Friendly

Avoid stereotypical "hacker" styling.

---

# Color Palette

## Background

Page

#12161C

Secondary Background

#1A2029

Card

#202734

---

## Borders

#313A49

Borders should define component separation.

Avoid glowing borders.

---

## Typography

Primary

#F4F7FA

Secondary

#A9B4C2

Muted

#7C8798

---

## Accent

Primary

#3A7BFF

Use only for

- Primary buttons
- Active navigation
- Links
- Focus states
- Interactive highlights

---

## Status Colors

Success

#22C55E

Warning

#FFB547

Danger

#E5484D

Info

#36C2FF

---

# Typography

Use **Inter** if it is not already loaded.

Improve typography by defining reusable font sizes, weights, and spacing.

Do not modify layouts.

---

# CSS Design Tokens

Create reusable CSS custom properties for:

Colors

Typography

Spacing

Border Radius

Shadows

Transitions

Focus Ring

Z-index layers (if needed)

Every future component should consume these variables instead of hardcoded values.

---

# Shadows

Avoid heavy shadows.

Use subtle elevation only.

Cards should appear separated through borders first, shadows second.

---

# Border Radius

Standard radius

16px

Small radius

8px

Buttons

12px

Inputs

12px

---

# Motion

Create reusable transition variables.

Animations should feel subtle and professional.

Avoid dramatic animations.

---

# Focus States

Use the primary blue accent.

Focus indicators should remain clearly visible for keyboard users.

Accessibility must not regress.

---

# Scope

This sprint establishes the global design system only.

Do NOT redesign

- Navigation
- Dashboard
- Reports
- Scan Detail
- Forms
- Cards
- Buttons
- Tables

Those belong to later sprints.

---

# Do NOT

Do NOT

- Modify Django views
- Modify models
- Modify URLs
- Modify scanner logic
- Modify JavaScript behavior
- Change page layouts
- Move components

Do not introduce backend changes.

---

# Files Allowed To Change

Primary

```
static/css/custom.css
```

If necessary

```
templates/base.html
```

Only for importing Inter or global stylesheet requirements.

No other files.

---

# Verification

Verify

✓ Dashboard renders correctly

✓ Scan Detail renders correctly

✓ Reports render correctly

✓ Navigation remains unchanged

✓ Existing Bootstrap components still function

✓ Responsive layouts remain intact

✓ Charts still render correctly

✓ No JavaScript regressions

✓ Django starts successfully

---

# Deliverables

At the end of this sprint ARGUS should have:

- A reusable design token system
- Midnight Slate color palette
- Global typography system
- Shadow system
- Border radius system
- Motion system
- Focus system

No individual page should be redesigned yet.

This sprint prepares the project for future UI improvements.

---

# Commit Message

```
style(ui): establish Midnight Slate design system
```

---

# Stop

After verification

STOP.

Do not redesign components.

Do not begin Navigation improvements.

Wait for the next sprint.