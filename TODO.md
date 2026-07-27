# ARGUS - CURRENT SPRINT

Status:
🚧 Active Development

Current Branch:

feature/scan-detail

---

# Current Goal

Upgrade the Scan Detail page without breaking existing functionality.

This sprint focuses ONLY on improving the existing page.

No backend architecture changes.

No database changes.

No authentication work.

No dashboard work.

No homepage work.

---

# Sprint Rules

One feature at a time.

Each completed feature must be

- implemented
- tested
- reviewed
- committed

before starting the next feature.

---

# Sprint Checklist

## Executive Summary

Status

⬜ Pending

Requirements

- Better project header
- Security grade
- Better risk score presentation
- Better scan metadata
- Better action buttons

Files

templates/scanner/scan_detail.html

static/css/custom.css

---

## Severity Cards

Status

⬜ Pending

Requirements

Improve

Critical

High

Medium

Low

Info

Cards

Hover effects

Responsive layout

No backend changes.

---

## Risk Score Card

Status

⬜ Pending

Requirements

Improve appearance

Better typography

Better spacing

Animated counter

No backend changes.

---

## Findings Cards

Status

⬜ Pending

Requirements

Improve

Spacing

Badges

Typography

Icons

Expandable details

Do not change backend variables.

---

## Code Snippet Viewer

Status

⬜ Pending

Requirements

Line numbers

Copy button

Highlighted vulnerable line

Scrollable

Dark theme

No syntax highlighting yet.

---

## Filters

Status

⬜ Pending

Requirements

Improve

Severity filter

Engine filter

Search

Responsive behavior

Do not rewrite filtering logic.

---

## Empty State

Status

⬜ Pending

Requirements

Professional empty state

No oversized whitespace

Responsive

---

## Mobile Responsiveness

Status

⬜ Pending

Requirements

Phones

Tablets

Desktop

---

## Cleanup

Status

⬜ Pending

Requirements

Remove duplicate CSS

Improve spacing

Remove unnecessary wrappers

No functionality changes

---

# Out of Scope

Do NOT work on

Dashboard

Homepage

Reports

Authentication

REST API

Docker

Repository Explorer

Secret Scanner

Dependency Scanner

AI Explanations

These belong to future sprints.

---

# Testing Checklist

Every completed feature must satisfy

☐ Django starts

☐ No template errors

☐ No console errors

☐ Charts render

☐ Buttons work

☐ Filters work

☐ Pagination works

☐ Responsive layout

☐ No extra scrolling

☐ No huge whitespace

☐ Existing functionality preserved

---

# Commit Strategy

One feature = One commit

Examples

feat(scan-detail): improve executive summary

feat(scan-detail): redesign findings cards

feat(scan-detail): improve risk score card

feat(scan-detail): improve filters

Never combine multiple unrelated features into one commit.

---

# Claude Instructions

Before editing

1. Inspect existing implementation.
2. Explain intended changes.
3. List files to modify.
4. Wait if changes affect more than two files.

After editing

1. Verify application runs.
2. Verify layout.
3. Verify functionality.
4. Stop.

Never continue to another feature automatically.