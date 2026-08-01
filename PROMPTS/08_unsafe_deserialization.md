# Phase 3 — Sprint 8

## Unsafe Deserialization Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement the fourth AST detection rule:

Unsafe Deserialization Detection.

The AST framework is already complete.

This sprint adds **one new rule only**.

No framework changes.

No architecture changes.

---

# Background

The following components are already complete and must remain unchanged:

- AST Engine
- Rule Registry
- BaseRule
- Finding Normalization
- Dangerous Function Rule
- Command Injection Rule
- SQL Injection Rule

This sprint extends the framework with one additional independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/deserialization.py

The rule must inherit from BaseRule.

Follow the same coding style, metadata structure, and finding format used by the existing AST rules.

---

# Detection Scope

Detect unsafe deserialization APIs using Python AST.

Supported APIs include:

## pickle

- pickle.load()
- pickle.loads()

## cPickle

- cPickle.load()
- cPickle.loads()

## dill

- dill.load()
- dill.loads()

## marshal

- marshal.load()
- marshal.loads()

## shelve

- shelve.open()

## yaml

- yaml.load()

Use AST node analysis.

Do not use:

- regular expressions
- plain text searching
- string matching alone

Resolve fully-qualified function calls in the same manner as the existing Command Injection rule.

---

# Safe Patterns

Do NOT report:

- yaml.safe_load()

or other explicitly safe deserialization APIs.

Only report APIs that are considered unsafe by default.

---

# Detection Rules

This sprint detects unsafe API usage only.

Do NOT implement:

- taint analysis
- trust-boundary analysis
- user-input tracking
- data-flow analysis
- symbolic execution
- runtime validation

Simply report usage of the unsafe APIs.

---

# Metadata

Provide metadata consistent with existing AST rules.

Include:

- id
- name
- description
- severity
- confidence
- cwe
- owasp

Use:

- CWE-502 (Deserialization of Untrusted Data)

Use the appropriate OWASP category consistent with the existing rules.

---

# Findings

Return findings using the existing normalized format.

Each finding should include:

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

Do not write directly to the database.

---

# Registration

Register the rule using the existing registration mechanism.

Do not redesign or modify the framework.

Do not modify:

- ast_engine.py
- registry.py
- base_rule.py
- findings.py

---

# Files Allowed To Change

Primary

scanner/engines/ast/rules/deserialization.py

If required by the existing registration mechanism

scanner/engines/ast/__init__.py

scanner/engines/ast/rules/__init__.py

No other files.

Specifically do NOT modify

- ast_engine.py
- registry.py
- base_rule.py
- findings.py
- services.py
- scanner/views.py
- scanner/models.py

---

# Verification

Verify:

✓ pickle.load()

✓ pickle.loads()

✓ cPickle.load()

✓ cPickle.loads()

✓ dill.load()

✓ dill.loads()

✓ marshal.load()

✓ marshal.loads()

✓ shelve.open()

✓ yaml.load()

✓ yaml.safe_load() is NOT reported

✓ Multiple unsafe deserialization calls generate multiple findings

✓ Safe Python code generates zero findings

✓ Existing Dangerous Function detection still works

✓ Existing Command Injection detection still works

✓ Existing SQL Injection detection still works

✓ Django starts successfully

✓ No regressions

---

# Deliverables

At the end of this sprint:

- One new independent Unsafe Deserialization rule exists.
- The rule integrates with the existing AST framework.
- No framework architecture has changed.
- Existing rules continue working unchanged.

---

# Commit Message

feat(ast): add unsafe deserialization detection rule

---

# Stop

After verification

STOP.

Do not refactor the AST framework.

Do not modify existing rules.

Do not begin Weak Cryptography Detection.