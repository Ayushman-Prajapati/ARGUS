# ARGUS - Sprint 8

## Feature

Scan Detail Cleanup & Production Readiness

---

# Context

Read the following files before making any changes.

.claude.md

PROJECT.md

ROADMAP.md

TODO.md

Review all previous Scan Detail improvements before making changes.

---

# Goal

Perform a final cleanup of the Scan Detail page.

Do NOT add new features.

Do NOT redesign the UI.

Do NOT modify backend logic.

This sprint focuses on consistency, maintainability, accessibility, and code quality.

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
- Findings
- Charts
- Risk Score
- Executive Summary
- Code Viewer
- Filters
- Pagination
- Buttons

Do not rename variables.

Do not change backend behavior.

---

# Cleanup Tasks

Review the Scan Detail page and improve

- HTML structure
- CSS organization
- Accessibility
- Spacing consistency
- Typography consistency
- Card alignment
- Responsive behavior
- Bootstrap utility usage

Do not redesign components.

---

# HTML Cleanup

Improve

- Semantic HTML
- Heading hierarchy
- Section organization
- Comments
- Readability
- Indentation

Remove

- Empty elements
- Unused wrappers
- Duplicate containers
- Redundant classes

Do not remove working template logic.

---

# CSS Cleanup

Review custom.css.

Remove

- Duplicate selectors
- Duplicate media queries
- Unused rules (only if confirmed unused)
- Redundant spacing

Group CSS into sections

Example

------------------------------------------------

Scan Detail

Executive Summary

Risk Score

Charts

Filters

Findings

Code Viewer

Responsive

------------------------------------------------

Use comments for organization.

---

# Accessibility

Improve accessibility where possible.

Include

- aria-label attributes
- Accessible buttons
- Proper heading order
- Focus visibility
- Keyboard-friendly controls

Do not introduce JavaScript.

---

# Bootstrap Usage

Prefer Bootstrap utilities.

Replace unnecessary custom CSS with Bootstrap classes where appropriate.

Avoid duplication.

---

# Visual Consistency

Verify

- Equal card spacing
- Equal border radius
- Consistent shadows
- Consistent typography
- Consistent badge styles
- Consistent icon spacing
- Consistent button sizes

---

# Performance

Review

- Excessive nesting
- Unnecessary wrappers
- Duplicate HTML
- Duplicate CSS

Optimize without changing behavior.

---

# Documentation

Add short comments before major sections.

Example

Executive Summary

Risk Score

Charts

Filters

Findings

Code Viewer

Avoid excessive commenting.

---

# CSS Rules

Maintain

Dark cyber theme

Minimal appearance

Professional SaaS look

Responsive layout

Avoid unnecessary CSS.

---

# HTML Rules

Preserve all Django template variables.

Do not rename blocks.

Do not modify template inheritance.

Do not modify forms.

---

# Before Editing

Inspect the page.

Explain

1. What cleanup opportunities exist.

2. Which files will be modified.

3. Why cleanup improves maintainability.

Do not write code yet.

---

# Implementation

Perform only cleanup tasks.

Do not introduce new functionality.

Do not redesign components.

---

# Final Verification

Verify

✓ Django starts successfully

✓ No template errors

✓ No console errors

✓ Charts work

✓ Filters work

✓ Pagination works

✓ Buttons work

✓ Responsive layout

✓ No duplicate CSS

✓ No unnecessary wrappers

✓ Accessibility improved

✓ Existing functionality preserved

---

# Deliverables

Provide

1. Files modified

2. Cleanup summary

3. Accessibility improvements

4. CSS improvements

5. HTML improvements

6. Remaining technical debt

Then STOP.

---

# Safety Rule

If any cleanup requires modifying forbidden files or changing application behavior, STOP and explain why instead of making risky changes.