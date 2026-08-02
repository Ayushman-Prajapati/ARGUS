# Phase 4 — Sprint 8

## Accessibility & Responsive Polish

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Improve the overall accessibility, responsiveness, and usability of ARGUS while preserving the established **Midnight Slate** design system.

This sprint focuses on usability improvements only.

Do not redesign pages.

Do not modify backend functionality.

---

# Background

The following have already been completed:

- Midnight Slate Design System
- Navigation Refresh
- Cards & Reusable Components
- Forms & Tables Refresh
- Dashboard Refresh
- Scan Detail Refresh
- Reports Refresh

This sprint reviews the entire application to improve accessibility and responsiveness.

---

# Scope

Review and improve:

- Keyboard Navigation
- Focus Indicators
- Color Contrast
- Typography Readability
- Responsive Layout
- Mobile Experience
- Tablet Experience
- Interactive Components
- Animations
- Reduced Motion Support

Preserve all existing functionality.

---

# Accessibility

Review every interactive component.

Ensure

- Every button is keyboard accessible.
- Every link is keyboard accessible.
- Form controls have visible focus indicators.
- Focus order is logical.
- Focus never becomes trapped.
- Interactive controls remain reachable.

Do not remove existing accessibility features.

---

# Color Contrast

Review the complete Midnight Slate theme.

Verify text contrast for:

- Primary text
- Secondary text
- Muted text
- Buttons
- Links
- Tables
- Forms
- Navigation
- Alerts
- Badges

Improve contrast where necessary.

Target WCAG AA compliance wherever practical.

---

# Typography

Review

- Heading hierarchy
- Line height
- Paragraph spacing
- Font sizes
- Readability

Do not change the established typography system unless necessary for accessibility.

---

# Responsive Review

Review all major pages.

Verify

- Dashboard
- Scan Detail
- Reports
- Authentication pages
- Forms
- Tables
- Navigation

Check common breakpoints.

Desktop

Tablet

Mobile

Improve spacing and wrapping where necessary.

Do not redesign layouts.

---

# Tables

Review responsive behavior.

Ensure

- Horizontal scrolling works correctly.
- Content remains readable.
- Headers remain visible.
- Overflow handling remains clean.

---

# Forms

Verify

- Mobile usability
- Touch targets
- Label alignment
- Validation messages
- File upload controls

---

# Navigation

Verify

- Mobile menu
- Sidebar (if present)
- Dropdown menus
- User menu

Maintain existing functionality.

---

# Animations

Review all transitions.

Ensure animations remain

- Short
- Smooth
- Professional

Avoid distracting effects.

---

# Reduced Motion

Respect users who prefer reduced motion.

Where appropriate

- Reduce transition duration
- Disable unnecessary animations
- Preserve usability

Do not remove meaningful interaction feedback.

---

# Empty States

Review every empty state.

Ensure

- Clear messaging
- Proper spacing
- Consistent typography

Do not add illustrations.

---

# Design Consistency

Review the application for inconsistencies.

Examples

- Different border radii
- Inconsistent spacing
- Mixed typography
- Misaligned components
- Different button styles
- Inconsistent hover states

Standardize them using the existing design system.

---

# Do NOT

Do NOT modify

- Django views
- Models
- URLs
- Scanner logic
- Authentication
- Reports generation
- AST Engine
- JavaScript functionality

Do not redesign pages.

Do not move components.

---

# Files Allowed To Change

Primary

```
static/css/custom.css
```

If necessary

```
templates/*
```

Only for accessibility improvements such as:

- ARIA attributes
- Semantic HTML
- Focus handling
- Minor responsive adjustments

Do not modify backend files.

---

# Verification

Verify

✓ Dashboard remains responsive

✓ Scan Detail remains responsive

✓ Reports remain responsive

✓ Navigation works on mobile

✓ Tables remain usable

✓ Forms remain usable

✓ Keyboard navigation works

✓ Focus indicators are visible

✓ Contrast remains accessible

✓ Charts continue functioning

✓ Existing functionality preserved

✓ Django starts successfully

---

# Deliverables

At the end of this sprint:

- ARGUS should provide a more accessible experience.
- Responsive behavior should be polished across all supported screen sizes.
- Interactive components should feel consistent.
- Keyboard navigation should work throughout the application.
- The Midnight Slate design system should remain visually consistent.

No backend behavior should change.

---

# Commit Message

```text
style(ui): improve accessibility and responsiveness
```

---

# Stop

After verification

STOP.

Do not begin final cleanup.

Wait for the next sprint.