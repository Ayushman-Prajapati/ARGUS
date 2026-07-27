# ARGUS – Sprint 5

## Feature

Improve Code Viewer

---

# Context

Read these files before making changes.

- .claude.md
- PROJECT.md
- ROADMAP.md
- TODO.md

Understand the project before writing code.

---

# Goal

Improve ONLY the Code Viewer section.

Do NOT redesign the page.

Do NOT modify backend logic.

The objective is to make code snippets significantly easier to read while preserving all existing functionality.

---

# Allowed Files

- templates/scanner/scan_detail.html
- static/css/custom.css

---

# Forbidden Files

- scanner/views.py
- scanner/models.py
- scanner/forms.py
- settings.py
- urls.py
- static/js/
- reports/

Do not modify any forbidden files.

---

# Missing Data Policy

Use ONLY existing Django template variables.

If any of the following are unavailable:

- language
- filename
- full file path
- vulnerable line
- line numbers

DO NOT

- create new template variables
- modify Python files
- create template filters
- add context variables

Instead

- display placeholders
- omit the element if necessary
- explain the limitation in the final report

---

# Preserve

Keep existing:

- Django template variables
- Findings
- Code snippets
- Filters
- Charts
- Buttons
- Pagination
- Collapse behavior

Do not rename template variables.

Do not modify backend logic.

---

# Required Improvements

Improve ONLY the Code Viewer UI.

Include:

- Monospace font
- Scrollable code container
- Rounded borders
- Better spacing
- Better typography
- Dark theme code panel
- File path header
- Language badge
- Copy Code button (visual only)

Optional:

- Line numbers ONLY if existing template data already supports them.
- Vulnerable line highlight ONLY if existing template data already identifies the vulnerable line.

Do NOT implement:

- Syntax highlighting
- Clipboard functionality
- JavaScript
- Backend logic

---

# Code Viewer Layout

------------------------------------------------

File Name

Full File Path

Language Badge

Copy Code Button

------------------------------------------------

Code Block

------------------------------------------------

Requirements

- Preserve indentation
- Horizontal scrolling
- No unnecessary wrapping
- Readable on smaller screens
- Consistent padding
- Rounded corners
- Compact spacing

---

# Code Block Styling

Use

- Dark background
- Subtle border
- Monospace font
- Comfortable line height
- Consistent padding
- Rounded corners

---

# HTML Rules

Modify ONLY the Code Viewer section.

Leave every other section untouched.

Use semantic HTML.

Preserve existing template logic.

Use exactly ONE `<summary>` element inside each `<details>`.

Do NOT:

- create nested `<details>`
- duplicate "View code snippet" controls
- change collapse behavior

---

# Copy Button Rules

The Copy Code button is visual only.

Do NOT add:

- JavaScript
- onclick handlers
- clipboard logic
- data attributes

It should only be a styled UI element.

---

# CSS Rules

Reuse existing CSS whenever possible.

Avoid duplicate styles.

Maintain the existing dark cyber theme.

Keep spacing compact.

Maintain responsiveness.

---

# Before Editing

Inspect the existing Code Viewer.

Explain:

1. Current implementation
2. Existing template variables available
3. Files to modify
4. Which requested features can be implemented using existing data
5. Which requested features cannot be implemented without backend changes

Wait for approval.

Do NOT edit any files.

---

# Implementation

After approval,

Implement ONLY the Code Viewer improvements.

Modify ONLY:

- templates/scanner/scan_detail.html
- static/css/custom.css

Do not continue to another feature.

Do not perform opportunistic UI improvements.

Stop immediately after the Code Viewer is complete.

---

# Verification

Verify:

✓ Code still displays correctly

✓ No template errors

✓ Responsive layout

✓ Existing functionality preserved

✓ No CSS regressions

✓ Horizontal scrolling works

✓ Long lines remain readable

✓ Exactly one `<summary>` inside every `<details>`

✓ No duplicate Code Viewer controls

✓ Existing collapse behavior preserved

---

# Final Report

Provide:

1. Files modified
2. Summary of improvements
3. Visual enhancements
4. Features intentionally skipped due to missing backend data
5. Confirmation that no backend files were modified

Then STOP.