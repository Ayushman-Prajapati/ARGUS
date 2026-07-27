# ARGUS - Sprint 2

## Feature

Improve Findings Cards

---

# Context

Read these files first.

.claude.md

PROJECT.md

ROADMAP.md

TODO.md

Understand the project before making changes.

---

# Goal

Improve ONLY the Findings section.

Do NOT redesign the page.

Do NOT modify any backend logic.

Improve readability and usability while preserving all existing functionality.

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

Do not modify any forbidden file.

---

# Preserve

Keep existing

Django template variables

Pagination

Filters

Buttons

Collapse behavior

Finding IDs

Context variables

Do not rename any variables.

---

# Required Improvements

Improve every Finding card.

Each card should clearly display

• Vulnerability title

• Severity badge

• Scanner engine

• CWE (if available)

• OWASP category (if available)

• File path

• Line number

• Confidence

• Risk indicator

• Description

• Remediation

• Code snippet

Maintain existing template variables.

If backend data does not exist, display a clean placeholder.

Do NOT modify Python code.

---

# Visual Improvements

Use cards instead of long text blocks.

Better spacing.

Consistent typography.

Improved badges.

Professional icons.

Better hierarchy.

Highlight severity with color accents.

Code snippets should appear inside a dedicated code block.

Keep the layout compact.

Avoid excessive whitespace.

---

# Code Snippet Section

Improve readability.

Include

• Monospace font

• Line number badge

• Copy button placeholder

• Horizontal scrolling

• Rounded container

Do not implement JavaScript copy functionality yet.

---

# CSS Rules

Reuse existing CSS.

Avoid duplicate styles.

Add only the minimum required CSS.

Maintain dark theme.

Maintain responsiveness.

---

# HTML Rules

Modify only the Findings section.

Leave the rest of the page untouched.

Use Bootstrap cards.

Use semantic HTML.

Keep Django template logic intact.

---

# Before Editing

Inspect the current Findings section.

Explain

1. What will change.

2. Files to modify.

3. Why these improvements help usability.

Do not write code yet.

---

# Implementation

Implement only the Findings section.

Do not modify any other section.

---

# Verification

Verify

✓ Existing findings still display correctly

✓ No template errors

✓ Pagination still works

✓ Filters still work

✓ Responsive layout

✓ No broken CSS

✓ No excessive whitespace

✓ Existing functionality preserved

---

# Final Report

Provide

1. Files modified

2. Summary of changes

3. Visual improvements made

4. Remaining limitations

Stop after completing this feature.