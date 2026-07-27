# ARGUS - Sprint 7

## Feature

Responsive Layout Optimization

---

# Context

Read the following files before making any changes.

.claude.md

PROJECT.md

ROADMAP.md

TODO.md

Understand the project before writing code.

---

# Goal

Improve ONLY the responsiveness of the Scan Detail page.

Do NOT redesign the page.

Do NOT modify backend logic.

Do NOT change template variables.

The objective is to make every section responsive while preserving existing functionality.

---

# Allowed Files

templates/scanner/scan_detail.html

static/css/custom.css

---

# Forbidden Files

scanner/views.py

scanner/models.py

scanner/forms.py

settings.py

urls.py

static/js/

reports/

Do not modify forbidden files.

---

# Preserve

Keep existing

- Django template variables
- Bootstrap layout
- Charts
- Findings
- Filters
- Buttons
- Pagination
- Code Viewer
- Risk Score

Do not rename variables.

Do not change business logic.

---

# Responsive Targets

Support

- Mobile (320px+)
- Large Mobile (480px+)
- Tablet (768px+)
- Laptop (1024px+)
- Desktop (1440px+)

The page should remain fully usable on every device.

---

# Required Improvements

Review every section and improve responsiveness.

Sections

- Executive Summary
- Risk Score
- Findings
- Code Viewer
- Filters
- Charts
- Buttons
- Metadata Cards

Only improve layout.

Do not redesign components.

---

# Mobile Layout

Cards should stack vertically.

Buttons should wrap naturally.

No horizontal scrolling.

Charts should resize automatically.

Filters should stack cleanly.

Long file paths should wrap gracefully.

Code snippets should remain scrollable horizontally.

---

# Tablet Layout

Use two-column layouts where appropriate.

Maintain consistent spacing.

Prevent oversized cards.

Avoid empty whitespace.

---

# Desktop Layout

Keep balanced spacing.

Maintain equal card heights.

Prevent stretched containers.

Align cards consistently.

Avoid unnecessary page width.

---

# Typography

Improve readability.

Prevent text overflow.

Prevent badge overlap.

Ensure headings scale appropriately.

Use Bootstrap typography utilities where possible.

---

# Images and Charts

Charts must remain responsive.

No fixed widths.

Maintain aspect ratio.

Do not modify Chart.js configuration.

---

# Tables and Code Blocks

Prevent layout breaking.

Allow horizontal scrolling only where appropriate.

Never overflow the page.

Maintain readable padding.

---

# Buttons

Buttons should

- wrap correctly
- remain aligned
- maintain consistent spacing
- avoid overlapping

---

# CSS Rules

Reuse Bootstrap responsive utilities.

Prefer Flexbox and Bootstrap Grid.

Avoid duplicate media queries.

Only add media queries when necessary.

Maintain dark cyber theme.

Avoid excessive spacing.

---

# HTML Rules

Only modify layout-related HTML.

Preserve all Django template logic.

Do not remove existing components.

Do not introduce unnecessary wrappers.

---

# Before Editing

Inspect the current responsive layout.

Explain

1. Which responsive issues were found.

2. Which files will be modified.

3. How responsiveness will improve.

Do not write code yet.

---

# Implementation

Implement only responsive improvements.

Do not redesign the UI.

Do not continue to another feature.

---

# Verification

Test the page at

✓ 320px

✓ 480px

✓ 768px

✓ 1024px

✓ 1440px

Verify

✓ No horizontal scrolling

✓ Charts resize correctly

✓ Cards stack correctly

✓ Buttons remain usable

✓ Filters remain usable

✓ Code viewer scrolls correctly

✓ No CSS regressions

✓ Existing functionality preserved

---

# Final Report

Provide

1. Files modified

2. Responsive improvements made

3. Breakpoints tested

4. Remaining limitations

Then STOP.

---

# Safety Rule

If improving responsiveness requires modifying forbidden files or redesigning the page, STOP and explain why instead of making risky changes.