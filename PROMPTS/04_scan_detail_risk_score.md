# ARGUS - Sprint 4

## Feature

Improve Risk Score Card

---

# Context

Read these files before making any changes.

.claude.md

PROJECT.md

ROADMAP.md

TODO.md

Understand the project before writing code.

---

# Goal

Improve ONLY the Risk Score section of the Scan Detail page.

Do NOT redesign the page.

Do NOT change any backend logic.

Improve the visual presentation while preserving existing functionality.

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

Do not modify any forbidden files.

---

# Preserve

Keep existing

- Django template variables
- Risk score calculation
- Charts
- Filters
- Findings
- Buttons
- Context variables

Do not rename variables.

Do not modify backend calculations.

---

# Required Improvements

Improve the Risk Score card.

Include

• Large risk score value

• Risk level badge

• Progress bar

• Circular gauge placeholder

• Short explanation

• Risk summary

• Better typography

• Better spacing

• Better hierarchy

Reuse existing template values whenever possible.

If backend values are unavailable, use placeholders instead of modifying Python code.

---

# Risk Levels

Display one of

Critical

High

Medium

Low

Informational

The badge styling should depend on the existing severity or score.

Do not calculate anything in the template.

---

# Progress Visualization

Use a Bootstrap progress bar.

Show percentage if available.

If not available, display a placeholder.

Do not introduce JavaScript.

---

# Summary Section

Display a short explanation.

Example

Overall project risk is High based on the current findings.

Use placeholders if backend data is unavailable.

---

# Layout

Desktop

--------------------------------

Risk Score

Badge

Progress

Summary

--------------------------------

Mobile

Everything stacks vertically.

---

# CSS Rules

Reuse existing CSS.

Maintain dark cyber theme.

Avoid duplicate styles.

Keep spacing compact.

Maintain responsiveness.

---

# HTML Rules

Modify only the Risk Score section.

Leave all other sections untouched.

Use semantic HTML.

Keep existing template logic.

---

# Before Editing

Inspect the existing Risk Score section.

Explain

1. What will change.

2. Which files will be modified.

3. Why these improvements improve readability.

Do not write code yet.

---

# Implementation

Implement only the Risk Score improvements.

Do not continue to another section.

---

# Verification

Verify

✓ Existing score displays correctly

✓ No template errors

✓ Responsive layout

✓ No CSS regressions

✓ Charts unaffected

✓ Filters unaffected

✓ Existing functionality preserved

---

# Final Report

Provide

1. Files modified

2. Summary of changes

3. Visual improvements

4. Remaining limitations

Then STOP.