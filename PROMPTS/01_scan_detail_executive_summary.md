# ARGUS - Sprint 1

## Feature

Executive Summary Redesign

---

# Context

Read the following files before writing any code.

.claude.md

PROJECT.md

ROADMAP.md

TODO.md

Understand the project architecture before making changes.

---

# Goal

Improve ONLY the Executive Summary section at the top of the Scan Detail page.

Do NOT redesign the entire page.

Do NOT replace the existing layout.

The objective is to improve the existing UI while preserving all functionality.

---

# Allowed Files

templates/scanner/scan_detail.html

static/css/custom.css

---

# Forbidden Files

scanner/views.py

scanner/models.py

scanner/forms.py

urls.py

settings.py

reports/

dashboard/

homepage/

static/js/

Do not modify any forbidden file.

---

# Preserve

Keep all existing

Django template variables

URLs

Forms

Buttons

Charts

Filters

Pagination

Risk score calculation

Context variables

Bootstrap grid

Do not rename anything.

---

# Required Improvements

Improve only the top section.

Include

• Better project title layout

• Better scan metadata

• Better action buttons

• Professional spacing

• Better typography

• Security Grade badge

• Better Risk Score presentation

• Scan Status badge

• Files Scanned

• Scan Duration

• Scan Date

• Source Type

• Enabled Scan Engines

Everything must use existing Django variables whenever possible.

If a value does not exist in the backend, create a placeholder instead of modifying Python code.

---

# UI Style

Professional

Minimal

Dark

Cyber Security

Modern SaaS

Inspired by

GitHub Security

Snyk

Linear

Do NOT copy any layout.

Use inspiration only.

---

# CSS Rules

Reuse existing variables.

Reuse Bootstrap.

Reuse existing classes whenever possible.

Only add new CSS if required.

Do not remove existing CSS.

Do not introduce unnecessary spacing.

Do not increase page height.

Maintain responsive behavior.

---

# HTML Rules

Improve existing HTML.

Do not replace the page.

Keep sections modular.

Use semantic HTML.

Use Bootstrap rows and columns.

Keep comments explaining major sections.

---

# Before Editing

Inspect the current page.

Explain

1. What will be changed.

2. Which files will be edited.

3. Why these changes are needed.

Do not write code yet.

---

# Implementation

After the explanation

Implement only the Executive Summary.

Do not continue to any other section.

---

# Verification

After implementation

Run Django.

Verify

✓ No template errors

✓ No console errors

✓ No CSS regressions

✓ No broken charts

✓ No broken filters

✓ No broken buttons

✓ No huge whitespace

✓ Responsive layout

✓ Existing functionality preserved

---

# Final Report

Provide

1. Files modified

2. Summary of changes

3. Screenshots or description of the visual improvements

4. Any limitations

Then STOP.

Do not continue implementing additional features.