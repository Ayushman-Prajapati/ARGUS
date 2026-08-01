# Phase 3 — Sprint 11

## AST Framework Finalization

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Finalize the ARGUS AST Framework.

This sprint focuses exclusively on:

- Testing
- Validation
- Documentation
- Cleanup

No new vulnerability detection.

No framework redesign.

No architecture changes.

---

# Background

The AST framework is complete.

Framework components:

- AST Engine
- Rule Registry
- BaseRule
- Finding Normalization
- Utilities

Implemented rules:

- Dangerous Functions
- Command Injection
- SQL Injection
- Unsafe Deserialization
- Hardcoded Secrets
- Weak Cryptography

The goal of this sprint is to improve reliability and prepare the framework for future expansion.

---

# Testing

Create comprehensive unit tests for every implemented AST rule.

Each rule should include:

## Positive Tests

Verify that vulnerable examples generate findings.

## Negative Tests

Verify that safe examples generate zero findings.

## Edge Cases

Include tests for:

- empty source
- empty file
- syntax errors
- nested functions
- nested classes
- aliases
- multiple findings in one file

---

# Engine Validation

Verify the complete pipeline.

Python Source

↓

AST Parsing

↓

Rule Registry

↓

Rule Execution

↓

Finding Normalization

↓

Returned Findings

Every stage should execute successfully.

---

# Finding Validation

Verify every rule returns the same normalized finding structure.

Every finding should consistently include:

- rule_id
- title
- description
- severity
- confidence
- cwe_id
- owasp_category
- line_number
- end_line_number
- code_snippet
- remediation

No rule should return a custom schema.

---

# Regression Testing

Verify existing functionality remains unchanged.

Existing rules:

✓ Dangerous Functions

✓ Command Injection

✓ SQL Injection

✓ Unsafe Deserialization

✓ Hardcoded Secrets

✓ Weak Cryptography

Verify the Django application still functions correctly.

Existing scan workflow must remain operational.

---

# Code Cleanup

Perform conservative cleanup only.

Allowed:

- remove dead code
- remove unused imports
- remove duplicated helper logic
- improve docstrings
- improve inline documentation
- improve type hints

Do NOT change behavior.

---

# Performance Review

Review for obvious inefficiencies only.

Examples:

- duplicated AST traversal
- unnecessary object creation
- repeated normalization

Only perform safe optimizations.

Do not redesign the architecture.

---

# Documentation

Update public module documentation where needed.

Ensure:

- classes have docstrings
- public methods have docstrings
- comments explain intent rather than restating code

Do not over-comment.

---

# Files Allowed To Change

Only files required for:

- tests
- documentation
- cleanup
- minor bug fixes discovered during testing

Do NOT modify:

- scanner/views.py
- scanner/models.py
- reports/
- templates/
- CSS
- JavaScript

Do not redesign the AST framework.

Do not modify public APIs unless required to fix a defect discovered during testing.

---

# Verification

Verify:

✓ All AST rule tests pass

✓ Existing rule behavior is preserved

✓ Empty projects scan successfully

✓ Invalid Python files are handled gracefully

✓ Safe code produces zero findings for provided test cases

✓ Existing scan pipeline works

✓ Django starts successfully

✓ No regressions

---

# Deliverables

At the end of this sprint:

- Every AST rule has unit tests.
- The framework has consistent finding structures.
- Documentation is complete.
- Dead code has been removed.
- The framework is stable and maintainable.
- No architectural changes have been introduced.

---

# Commit Message

chore(ast): finalize framework with tests and cleanup

---

# Stop

After verification:

1. Ensure all tests pass.
2. Review the feature branch.
3. Prepare the branch for merge into `main`.

Do not implement new detection rules.

Do not redesign the framework.

Phase 3 is complete.