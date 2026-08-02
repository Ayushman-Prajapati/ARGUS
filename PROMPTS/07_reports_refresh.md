# Phase 4 — Sprint 7

## Reports Refresh

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Modernize the Reports experience using the established **Midnight Slate** design system.

This sprint focuses exclusively on report presentation.

The goal is to improve readability, professionalism, and information hierarchy while preserving every existing report feature and export capability.

Do not modify report generation logic.

Do not modify backend functionality.

---

# Background

The following have already been completed:

- Midnight Slate Design System
- Navigation Refresh
- Cards & Reusable Components
- Forms & Tables Refresh
- Dashboard Refresh
- Scan Detail Refresh

This sprint applies the design system to all report-related pages.

---

# Scope

Refresh the appearance of:

- Report Header
- Executive Summary
- Risk Metrics
- Severity Summary
- Findings Tables
- Charts
- Code Snippets
- Recommendation Sections
- Print Layout (CSS only)

Preserve all existing report functionality.

---

# Report Header

Improve

- Report title
- Project information
- Scan metadata
- Generated date
- Visual hierarchy
- Spacing

The report should immediately communicate that it is a professional security assessment.

---

# Executive Summary

Improve

- Typography
- Card styling
- Section spacing
- Supporting text
- Visual hierarchy

Do not modify generated content.

---

# Risk Metrics

Improve

- Risk Score presentation
- Severity distribution
- Summary cards
- Labels
- Supporting information

Maintain all existing calculations.

---

# Findings Tables

Improve

- Header styling
- Row spacing
- Cell padding
- Typography
- Borders
- Hover state (HTML reports only)

Avoid zebra striping.

Maintain existing sorting and grouping.

---

# Severity Indicators

Use the established severity palette.

Critical

#E5484D

High

#FF8A3D

Medium

#FFB547

Low

#36C2FF

Info

#8895A7

Maintain consistent styling with the Dashboard and Scan Detail pages.

---

# Charts

Improve styling only.

Do not modify Chart.js logic.

Update

- Colors
- Grid lines
- Legends
- Tooltips
- Labels

Charts should visually match the rest of ARGUS.

---

# Code Snippets

Improve

- Background
- Borders
- Typography
- Padding
- Scrollbars
- Syntax readability

Do not modify syntax highlighting logic.

---

# Recommendation Sections

Improve

- Headings
- Lists
- Paragraph spacing
- Callout styling

Maintain existing report content.

---

# Print Layout

Review print-specific styling.

Ensure

- Good page breaks
- Consistent typography
- Printable tables
- Printable charts
- Readable spacing

Do not modify PDF generation logic.

Only improve presentation through CSS.

---

# Responsive Behavior

Verify

- HTML reports remain responsive.
- Tables remain usable.
- Charts resize correctly.
- Long findings remain readable.

Do not redesign the layout.

---

# Accessibility

Ensure

- WCAG-friendly contrast
- Readable typography
- Visible focus indicators (HTML reports)
- Severity is not communicated by color alone

---

# Design Rules

Use only the Midnight Slate design tokens.

Avoid

- Heavy shadows
- Large gradients
- Neon colors
- Decorative effects
- Glassmorphism

Prefer

- Professional typography
- Soft borders
- Consistent spacing
- Clean visual hierarchy

---

# Do NOT

Do NOT modify

- Django views
- Report generation logic
- Models
- URLs
- Scanner logic
- Authentication
- Risk calculations
- Export functionality

Do not redesign report layouts.

Do not introduce new report sections.

---

# Files Allowed To Change

Primary

```
static/css/custom.css
```

If necessary

```
templates/reports/*
```

Only for semantic improvements or styling hooks.

Do not modify backend files.

---

# Verification

Verify

✓ HTML reports render correctly

✓ PDF reports remain functional

✓ Executive Summary displays correctly

✓ Findings tables render correctly

✓ Charts continue functioning

✓ Code snippets remain readable

✓ Responsive layout preserved

✓ Print layout remains clean

✓ Accessibility maintained

✓ Django starts successfully

---

# Deliverables

At the end of this sprint:

- Reports should have a polished enterprise appearance.
- Executive Summary should have improved hierarchy.
- Findings should be easier to read.
- Charts should match the Midnight Slate design language.
- Print output should remain professional.

No backend behavior should change.

---

# Commit Message

```text
style(reports): refresh reporting interface
```

---

# Stop

After verification

STOP.

Do not begin Accessibility improvements.

Wait for the next sprint.
```