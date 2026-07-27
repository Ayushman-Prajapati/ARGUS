# ARGUS - Sprint 3

## Feature

Improve Findings Filters

---

# Context

Read these files before making any changes.

.claude.md

PROJECT.md

ROADMAP.md

TODO.md

Understand the project architecture before editing.

---

# Goal

Improve ONLY the filter section of the Scan Detail page.

Do NOT redesign the page.

Do NOT change backend logic.

Improve usability while preserving all existing functionality.

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
- Filter functionality
- Buttons
- Pagination
- Charts
- Findings

Do not rename variables.

Do not modify JavaScript.

---

# Required Improvements

Improve the filter toolbar.

Include

• Search input

• Severity dropdown

• Engine dropdown

• Clear Filters button

• Active filter indicators

• Findings count

• Better spacing

• Better alignment

Use Bootstrap components.

---

# Filter Layout

Desktop

-----------------------------------------------

Search

Severity

Engine

Clear Filters

Results Count

-----------------------------------------------

Mobile

Search

Severity

Engine

Clear Filters

Results Count

Everything should stack cleanly.

---

# Search Input

Improve appearance.

Include

- Search icon placeholder
- Rounded borders
- Proper spacing
- Responsive width

Do not implement new search logic.

Reuse existing functionality.

---

# Severity Filter

Improve dropdown styling.

Display severity badges where appropriate.

Do not modify filter logic.

---

# Engine Filter

Improve styling.

Use compact dropdown.

Preserve existing values.

---

# Results Counter

Display

Showing X Findings

Use existing template values whenever possible.

If unavailable, display a placeholder.

Do not modify backend.

---

# CSS Rules

Reuse Bootstrap.

Avoid duplicate styles.

Maintain dark theme.

Maintain responsive layout.

Do not increase page height unnecessarily.

---

# HTML Rules

Only modify the filter section.

Leave the rest of the page untouched.

Keep existing template logic.

Use semantic HTML.

---

# Before Editing

Inspect the existing filter section.

Explain

1. What will change.

2. Files to modify.

3. Why these improvements improve usability.

Do not write code yet.

---

# Implementation

Implement only the filter improvements.

Do not continue to another section.

---

# Verification

Verify

✓ Filters still work

✓ Search still works

✓ No template errors

✓ Responsive layout

✓ No CSS regressions

✓ Pagination unaffected

✓ Existing functionality preserved

---

# Final Report

Provide

1. Files modified

2. Summary of improvements

3. Any limitations

Then STOP.