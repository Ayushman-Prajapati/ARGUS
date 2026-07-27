# ARGUS - Sprint 6

## Feature

Improve Charts Section

---

# Context

Read these files before making changes.

.claude.md

PROJECT.md

ROADMAP.md

TODO.md

Understand the project before writing code.

---

# Goal

Improve ONLY the Charts section of the Scan Detail page.

Do NOT redesign the page.

Do NOT modify Chart.js logic.

Do NOT change backend calculations.

The objective is to improve readability and presentation.

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

- Chart.js configuration
- Django template variables
- Data sources
- Risk calculations
- Filters
- Buttons

Do not rename variables.

---

# Required Improvements

Improve the presentation of all charts.

Include

• Card headers

• Chart titles

• Chart descriptions

• Better spacing

• Better alignment

• Responsive sizing

• Consistent card heights

• Better legends

• Empty state when no data exists

Do not modify chart data.

---

# Chart Cards

Each chart should appear inside a professional card.

Each card should contain

- Title
- Short description
- Chart
- Footer (optional)

Maintain consistent spacing.

---

# Layout

Desktop

--------------------------------

Severity Chart

Engine Chart

--------------------------------

Both cards should have equal height.

Mobile

Charts stack vertically.

No horizontal scrolling.

---

# Empty State

If chart data is unavailable

Display

"No data available"

with a professional placeholder.

Do not modify backend.

---

# CSS Rules

Reuse existing styles.

Maintain dark cyber theme.

Avoid duplicate CSS.

Keep spacing compact.

Maintain responsiveness.

---

# HTML Rules

Modify only the Charts section.

Do not modify any other section.

Preserve existing template logic.

Use semantic HTML.

---

# Before Editing

Inspect the current Charts section.

Explain

1. What will change.

2. Files to modify.

3. Why these changes improve usability.

Do not write code yet.

---

# Implementation

Implement only the chart presentation improvements.

Do not continue to another feature.

---

# Verification

Verify

✓ Charts render correctly

✓ No JavaScript errors

✓ Responsive layout

✓ Equal card heights

✓ Existing functionality preserved

✓ No CSS regressions

---

# Final Report

Provide

1. Files modified

2. Summary of improvements

3. Visual enhancements

4. Remaining limitations

Then STOP.