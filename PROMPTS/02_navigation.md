# Phase 4 — Sprint 2

## Navigation Refresh

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Modernize the navigation experience of ARGUS using the newly established **Midnight Slate** design system.

This sprint focuses exclusively on the application's navigation components.

The objective is to improve visual hierarchy, usability, and consistency while preserving the existing navigation structure and functionality.

No backend changes.

No layout redesign.

---

# Background

The Midnight Slate design tokens have already been introduced.

This sprint applies those tokens to the navigation.

Existing navigation works correctly and should remain functionally identical.

---

# Scope

Refresh the appearance of:

- Top Navigation Bar
- Sidebar (if present)
- Navigation Links
- Active Navigation State
- Hover State
- Logo Area
- User Profile Menu
- Breadcrumbs (if present)

Preserve all existing routing and navigation behavior.

---

# Visual Goals

The navigation should feel:

- Professional
- Clean
- Enterprise
- Lightweight
- Information Dense
- Consistent

Take inspiration from:

- GitHub
- Linear
- Vercel
- Snyk

Do not copy their layouts.

---

# Navigation Bar

Improve:

- Background
- Height
- Padding
- Alignment
- Border
- Typography
- Hover transitions

The navigation should clearly separate itself from the page content using subtle borders instead of shadows.

---

# Sidebar

If the project contains a sidebar:

Improve

- Background
- Active item
- Hover state
- Section headings
- Icon spacing
- Text spacing
- Selected indicator

The sidebar should remain compact and easy to scan.

---

# Navigation Links

Improve

- Font weight
- Padding
- Hover feedback
- Active state
- Border radius

Active links should use the primary blue accent while maintaining good contrast.

Avoid glowing effects.

---

# User Menu

Improve

- Dropdown styling
- Avatar spacing
- Hover states
- Divider styling

Preserve existing functionality.

---

# Breadcrumbs

If breadcrumbs exist:

Improve

- Typography
- Spacing
- Separators
- Active page emphasis

Do not change navigation hierarchy.

---

# Mobile Navigation

Review responsive behavior.

Verify:

- Navigation remains usable.
- Dropdowns still work.
- Sidebar collapse (if applicable) still functions.

Do not redesign the mobile layout.

---

# Accessibility

Ensure

- Keyboard navigation remains functional.
- Focus indicators remain visible.
- Contrast remains WCAG-friendly.
- Active navigation is distinguishable without relying solely on color.

---

# Design Rules

Use only the design tokens introduced in Sprint 1.

Do not introduce new colors.

Do not hardcode values already defined as CSS variables.

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
- JavaScript functionality

Do not move navigation items.

Do not add new pages.

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

Any shared navigation templates used by the application.

Do not modify unrelated templates.

---

# Verification

Verify

✓ Navigation renders correctly

✓ Active navigation works

✓ Hover states work

✓ Dropdown menus function correctly

✓ Mobile navigation remains functional

✓ Responsive behavior preserved

✓ Accessibility maintained

✓ Existing routes unchanged

✓ Django starts successfully

---

# Deliverables

At the end of this sprint the navigation should:

- Match the Midnight Slate design system
- Feel modern and professional
- Have improved spacing and hierarchy
- Preserve all existing functionality
- Remain fully responsive

No page layouts should change.

---

# Commit Message

```text
style(ui): modernize navigation
```

---

# Stop

After verification

STOP.

Do not begin refreshing cards or buttons.

Wait for the next sprint.# Phase 4 — Sprint 2

## Navigation Refresh

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Modernize the navigation experience of ARGUS using the newly established **Midnight Slate** design system.

This sprint focuses exclusively on the application's navigation components.

The objective is to improve visual hierarchy, usability, and consistency while preserving the existing navigation structure and functionality.

No backend changes.

No layout redesign.

---

# Background

The Midnight Slate design tokens have already been introduced.

This sprint applies those tokens to the navigation.

Existing navigation works correctly and should remain functionally identical.

---

# Scope

Refresh the appearance of:

- Top Navigation Bar
- Sidebar (if present)
- Navigation Links
- Active Navigation State
- Hover State
- Logo Area
- User Profile Menu
- Breadcrumbs (if present)

Preserve all existing routing and navigation behavior.

---

# Visual Goals

The navigation should feel:

- Professional
- Clean
- Enterprise
- Lightweight
- Information Dense
- Consistent

Take inspiration from:

- GitHub
- Linear
- Vercel
- Snyk

Do not copy their layouts.

---

# Navigation Bar

Improve:

- Background
- Height
- Padding
- Alignment
- Border
- Typography
- Hover transitions

The navigation should clearly separate itself from the page content using subtle borders instead of shadows.

---

# Sidebar

If the project contains a sidebar:

Improve

- Background
- Active item
- Hover state
- Section headings
- Icon spacing
- Text spacing
- Selected indicator

The sidebar should remain compact and easy to scan.

---

# Navigation Links

Improve

- Font weight
- Padding
- Hover feedback
- Active state
- Border radius

Active links should use the primary blue accent while maintaining good contrast.

Avoid glowing effects.

---

# User Menu

Improve

- Dropdown styling
- Avatar spacing
- Hover states
- Divider styling

Preserve existing functionality.

---

# Breadcrumbs

If breadcrumbs exist:

Improve

- Typography
- Spacing
- Separators
- Active page emphasis

Do not change navigation hierarchy.

---

# Mobile Navigation

Review responsive behavior.

Verify:

- Navigation remains usable.
- Dropdowns still work.
- Sidebar collapse (if applicable) still functions.

Do not redesign the mobile layout.

---

# Accessibility

Ensure

- Keyboard navigation remains functional.
- Focus indicators remain visible.
- Contrast remains WCAG-friendly.
- Active navigation is distinguishable without relying solely on color.

---

# Design Rules

Use only the design tokens introduced in Sprint 1.

Do not introduce new colors.

Do not hardcode values already defined as CSS variables.

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
- JavaScript functionality

Do not move navigation items.

Do not add new pages.

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

Any shared navigation templates used by the application.

Do not modify unrelated templates.

---

# Verification

Verify

✓ Navigation renders correctly

✓ Active navigation works

✓ Hover states work

✓ Dropdown menus function correctly

✓ Mobile navigation remains functional

✓ Responsive behavior preserved

✓ Accessibility maintained

✓ Existing routes unchanged

✓ Django starts successfully

---

# Deliverables

At the end of this sprint the navigation should:

- Match the Midnight Slate design system
- Feel modern and professional
- Have improved spacing and hierarchy
- Preserve all existing functionality
- Remain fully responsive

No page layouts should change.

---

# Commit Message

```text
style(ui): modernize navigation
```

---

# Stop

After verification

STOP.

Do not begin refreshing cards or buttons.

Wait for the next sprint.