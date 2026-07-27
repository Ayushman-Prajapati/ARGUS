# ARGUS - Sprint 5

## Feature

Improve Code Viewer

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

Improve ONLY the Code Viewer section.

Do NOT redesign the page.

Do NOT modify backend logic.

The objective is to make code snippets easier to read while preserving all existing functionality.

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
- Code snippets
- Findings
- Filters
- Charts
- Buttons
- Pagination

Do not rename template variables.

Do not change backend logic.

---

# Required Improvements

Improve the code snippet display.

Include

• Monospace font

• Line numbers

• Highlight vulnerable line

• Scrollable code container

• Copy Code button (UI only)

• File path header

• Language badge

• Rounded borders

• Better spacing

• Better typography

Do not implement syntax highlighting.

Do not implement copy functionality.

Only improve the UI.

---

# Layout

--------------------------------

File Path

Language Badge

Copy Button

-------------------------------

Code Block

--------------------------------

The code block should

- scroll horizontally
- preserve indentation
- wrap only when appropriate
- remain readable on small screens

---

# Code Block Styling

Use

- dark background
- subtle border
- monospace font
- consistent padding
- line spacing
- rounded corners

Highlight the vulnerable line with a subtle background color.

---

# File Header

Display

- File name
- Full file path
- Language
- Line number

Reuse existing template variables.

If unavailable, display placeholders.

Do not modify backend.

---

# CSS Rules

Reuse existing CSS.

Avoid duplicate styles.

Maintain dark cyber theme.

Keep spacing compact.

Maintain responsiveness.

---

# HTML Rules

Modify only the Code Viewer section.

Leave the rest of the page untouched.

Use semantic HTML.

Preserve existing template logic.

---

# Before Editing

Inspect the existing Code Viewer.

Explain

1. What will change.

2. Files to modify.

3. Why these improvements improve readability.

Do not write code yet.

---

# Implementation

Implement only the Code Viewer improvements.

Do not continue to another feature.

---

# Verification

Verify

✓ Code still displays correctly

✓ No template errors

✓ Responsive layout

✓ Existing functionality preserved

✓ No CSS regressions

✓ Horizontal scrolling works

✓ Long lines remain readable

---

# Final Report

Provide

1. Files modified

2. Summary of improvements

3. Visual enhancements

4. Remaining limitations

Then STOP.