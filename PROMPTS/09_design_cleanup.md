# Phase 4 — Sprint 9

## Design System Cleanup & Final Polish

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Finalize the **Midnight Slate** design system and prepare ARGUS for the next development phase.

This sprint focuses on cleanup, consistency, maintainability, and quality assurance.

Do not introduce new UI features.

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
- Accessibility & Responsive Polish

This sprint prepares the design system for long-term maintenance.

---

# Scope

Perform a complete review of the UI and design system.

Focus on:

- Design consistency
- CSS cleanup
- Component consistency
- Design token usage
- Code quality
- Documentation
- Performance
- Cross-browser validation

---

# CSS Cleanup

Review the stylesheet and remove:

- Duplicate selectors
- Duplicate declarations
- Unused variables
- Unused utility classes
- Obsolete comments
- Dead CSS
- Inconsistent naming

Do not remove styles that are still referenced.

---

# Design Token Review

Ensure every component uses the design tokens introduced in Sprint 1.

Avoid hardcoded:

- Colors
- Border radius
- Shadows
- Typography
- Spacing
- Transitions

Replace duplicated values with existing CSS variables where appropriate.

---

# Visual Consistency

Review the entire application.

Verify consistency across:

- Navigation
- Dashboard
- Scan Detail
- Reports
- Forms
- Tables
- Cards
- Buttons
- Alerts
- Badges
- Code Viewer

Everything should feel like a single, cohesive product.

---

# Component Audit

Review reusable components.

Ensure consistent:

- Padding
- Margins
- Typography
- Hover states
- Focus states
- Disabled states
- Border radius
- Shadows

Do not redesign components.

---

# Performance Review

Review the CSS for obvious inefficiencies.

Examples

- Duplicate rules
- Overly specific selectors
- Unnecessary overrides
- Redundant declarations

Perform only safe optimizations.

Do not redesign the stylesheet.

---

# Documentation

Update comments where appropriate.

Document:

- Global design tokens
- Component organization
- Utility classes

Avoid excessive comments that simply restate the code.

---

# Browser Compatibility

Verify the interface remains functional in modern browsers.

Review

- Chrome
- Edge
- Firefox

No browser-specific hacks unless absolutely necessary.

---

# Regression Review

Verify the following remain fully functional.

Dashboard

✓ Statistics Cards

✓ Charts

✓ Quick Actions

✓ Activity Timeline

---

Scan Detail

✓ Executive Summary

✓ Findings

✓ Filters

✓ Code Viewer

---

Reports

✓ Report Layout

✓ Tables

✓ Charts

✓ PDF Styling

---

Navigation

✓ Navbar

✓ Sidebar (if present)

✓ User Menu

✓ Mobile Navigation

---

Forms

✓ Inputs

✓ Search

✓ Filters

✓ Upload Controls

---

Responsive Layout

✓ Desktop

✓ Tablet

✓ Mobile

---

# Accessibility Review

Perform a final review.

Ensure

- Keyboard navigation works.
- Focus indicators remain visible.
- Contrast remains accessible.
- Interactive elements remain usable.
- Typography remains readable.

No accessibility regressions should be introduced.

---

# Do NOT

Do NOT modify

- Django views
- Models
- URLs
- Scanner logic
- Authentication
- Report generation
- AST Engine
- JavaScript behavior

Do not introduce new features.

Do not redesign pages.

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

Only for:

- Minor cleanup
- Semantic improvements
- Removing redundant classes
- Improving maintainability

Do not modify backend files.

---

# Verification

Verify

✓ Dashboard renders correctly

✓ Scan Detail renders correctly

✓ Reports render correctly

✓ Navigation remains functional

✓ Charts continue functioning

✓ Forms continue functioning

✓ Responsive layouts preserved

✓ Accessibility maintained

✓ No CSS regressions

✓ No backend regressions

✓ Django starts successfully

---

# Deliverables

At the end of this sprint:

- The Midnight Slate design system should be fully implemented.
- The UI should have a consistent enterprise appearance.
- CSS should be clean, maintainable, and reusable.
- Design tokens should be used consistently across the application.
- ARGUS should be visually cohesive and ready for future feature development.

This sprint completes **Phase 4 — Design Refresh**.

---

# Commit Message

```text
style(ui): finalize Midnight Slate design system
```

---

# Stop

After verification:

1. Ensure all pages render correctly.
2. Review the feature branch.
3. Prepare the branch for merge into `main`.
4. Update `README.md`, `PROJECT.md`, `ROADMAP.md`, `TODO.md`, and `.claude.md` if required.

Do not begin the next development phase.

Wait for the next prompt.