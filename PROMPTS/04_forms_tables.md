# Phase 4 — Sprint 4

## Forms & Tables Refresh

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Modernize the forms and data presentation throughout ARGUS using the established **Midnight Slate** design system.

This sprint focuses exclusively on form controls and table components.

The objective is to improve readability, usability, accessibility, and consistency without changing any application logic.

Do not redesign pages.

Do not modify backend functionality.

---

# Background

The following have already been completed:

- Midnight Slate Design System
- Navigation Refresh
- Cards & Reusable Components

This sprint applies the design system to every form and table across the application.

---

# Scope

Refresh the appearance of:

- Text Inputs
- Password Inputs
- Search Inputs
- Select Dropdowns
- Textareas
- Checkboxes
- Radio Buttons
- File Upload Controls
- Input Groups
- Tables
- Pagination
- Filters
- Search Bars

Maintain all existing functionality.

---

# Forms

Improve

- Input background
- Borders
- Border radius
- Padding
- Typography
- Placeholder styling
- Disabled state
- Read-only state

Use subtle borders rather than heavy shadows.

---

# Focus States

Focus indicators should

- Use the Midnight Slate primary blue
- Be clearly visible
- Meet accessibility requirements

Avoid glowing effects.

---

# Validation States

Improve visual feedback for

- Valid inputs
- Invalid inputs
- Error messages
- Help text

Maintain existing validation logic.

---

# File Upload Controls

Improve

- Upload area
- Buttons
- Labels
- Drag-and-drop styling (if present)

Do not modify upload functionality.

---

# Search Inputs

Improve

- Search bars
- Filter inputs
- Clear visual hierarchy
- Placeholder readability

Maintain all existing filtering behavior.

---

# Tables

Improve

- Header styling
- Row spacing
- Cell padding
- Typography
- Borders
- Hover state

Avoid zebra striping.

Hover state should use a subtle blue tint.

Tables should remain information dense while improving readability.

---

# Pagination

Improve

- Previous/Next buttons
- Active page
- Hover state
- Disabled state

Preserve all pagination behavior.

---

# Filters

Refresh

- Severity filters
- Engine filters
- Search filters
- Sort controls

Maintain existing functionality.

---

# Responsive Behavior

Verify

- Tables remain usable on smaller screens.
- Forms remain responsive.
- Overflow handling remains functional.
- Existing layouts are preserved.

Do not redesign mobile layouts.

---

# Accessibility

Ensure

- Keyboard navigation works.
- Labels remain associated with controls.
- Placeholder text has sufficient contrast.
- Tables remain readable.
- Focus indicators remain visible.

Maintain WCAG-friendly contrast.

---

# Design Rules

Use only the Midnight Slate design tokens.

Avoid

- Heavy shadows
- Neon colors
- Large gradients
- Glassmorphism

Prefer

- Consistent spacing
- Clean typography
- Soft borders
- Subtle transitions

---

# Do NOT

Do NOT modify

- Django views
- Models
- URLs
- Scanner logic
- Reports
- Authentication
- Dashboard layout
- JavaScript behavior

Do not move components.

Do not redesign pages.

---

# Files Allowed To Change

Primary

```
static/css/custom.css
```

If necessary

Shared templates containing reusable form or table components.

Do not modify unrelated templates.

---

# Verification

Verify

✓ Forms render correctly

✓ Validation still works

✓ Search inputs function correctly

✓ Filters function correctly

✓ Tables remain readable

✓ Pagination works

✓ Responsive layouts preserved

✓ Accessibility maintained

✓ Existing functionality preserved

✓ Django starts successfully

---

# Deliverables

At the end of this sprint:

- Forms should feel modern and professional.
- Tables should be easier to read.
- Search and filter controls should be visually consistent.
- Pagination should integrate with the Midnight Slate design language.
- Accessibility should be preserved.

No backend behavior should change.

---

# Commit Message

```text
style(ui): improve forms and tables
```

---

# Stop

After verification

STOP.

Do not begin Dashboard Refresh.

Wait for the next sprint.
```