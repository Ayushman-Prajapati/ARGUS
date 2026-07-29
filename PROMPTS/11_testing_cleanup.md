# Phase 3 — Sprint 11

## Testing, Validation & Cleanup

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Finalize the ARGUS AST Framework by improving reliability, maintainability, and code quality.

This sprint focuses on testing, cleanup, validation, and documentation.

Do not introduce new vulnerability categories.

---

# Background

The AST framework now contains:

- AST Engine
- Rule Registry
- BaseRule
- Findings
- Utilities

Implemented rules:

- Dangerous Functions
- Command Injection
- SQL Injection
- Unsafe Deserialization
- Secret Detection
- Weak Cryptography

This sprint prepares the framework for production use.

---

# Testing

Create comprehensive unit tests for every AST rule.

Verify both positive and negative cases.

Every rule should include:

- Valid detection examples
- Safe code examples
- Edge cases
- Empty file handling
- Syntax error handling

The goal is to ensure reliable behavior across common scenarios.

---

# Engine Validation

Verify the complete pipeline.

Source Code

↓

Python AST

↓

Rule Registry

↓

Rule Execution

↓

Finding Collection

↓

Returned Findings

Ensure every stage functions correctly.

---

# Finding Consistency

Verify that every rule returns findings using the same structure.

Ensure consistent fields such as:

- rule id
- title
- description
- severity
- confidence
- CWE
- OWASP
- line number
- code snippet (if supported)

No rule should return a custom format.

---

# Code Quality

Review the AST framework and remove:

- dead code
- unused imports
- duplicated logic
- unnecessary helper functions
- obsolete comments

Improve readability where appropriate without changing behavior.

---

# Documentation

Update module docstrings and inline documentation where needed.

Ensure public classes and methods have clear documentation.

Avoid excessive comments that simply restate the code.

---

# Performance Review

Review the implementation for obvious inefficiencies.

Examples include:

- repeated AST traversal
- duplicated parsing
- unnecessary object creation

Only perform safe optimizations.

Do not redesign the architecture.

---

# Regression Testing

Verify:

✓ Existing Django application works

✓ Existing authentication works

✓ Existing dashboard works

✓ Existing Bandit integration works

✓ Existing Semgrep integration works

✓ Existing reports work

✓ Existing scan history works

✓ Existing project isolation works

✓ Existing UI works

No regressions should be introduced.

---

# Do NOT

Do NOT implement

- New vulnerability categories
- Taint analysis
- Data flow analysis
- Interprocedural analysis
- Symbol resolution
- Constant propagation
- AI-assisted detection

Those belong to future phases.

---

# Files Allowed To Change

Only files necessary for:

- tests
- documentation
- cleanup
- minor refactoring

Do not redesign the framework.

Do not change public APIs unless necessary to fix defects.

---

# Deliverables

The AST framework should be:

- fully tested
- well documented
- consistent
- maintainable
- production ready

All implemented rules should function correctly.

The overall architecture should remain unchanged.

---

# Verification Checklist

Verify:

✓ All implemented rules execute successfully

✓ Every rule produces consistent findings

✓ Empty projects scan successfully

✓ Invalid Python files are handled gracefully

✓ Safe code produces zero false positives for provided test cases

✓ Existing scan functionality remains operational

✓ Django starts successfully

✓ No regressions are introduced

---

# Commit Message

chore(ast): finalize framework with tests and cleanup

---

# Stop

After verification:

1. Ensure all tests pass.
2. Review the feature branch.
3. Prepare the branch for merge into `main`.

Do not implement additional detection rules or architectural changes.