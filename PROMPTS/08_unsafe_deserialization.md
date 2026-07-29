# Phase 3 — Sprint 8

## Unsafe Deserialization Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement an Unsafe Deserialization detection rule for the ARGUS AST Framework.

This rule should identify Python APIs that deserialize untrusted data and may lead to arbitrary code execution.

The implementation must integrate with the existing AST framework.

Do not modify the engine architecture.

---

# Background

The AST framework already contains:

- AST Engine
- Rule Registry
- BaseRule
- Dangerous Functions Rule
- Command Injection Rule
- SQL Injection Rule

This sprint introduces a new independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/deserialization.py

Create a rule that inherits from BaseRule.

The rule should analyze Python AST nodes and detect unsafe deserialization APIs.

---

# Detect

Detect usage of unsafe deserialization APIs including:

pickle.load()

pickle.loads()

cPickle.load()

cPickle.loads()

dill.load()

dill.loads()

marshal.load()

marshal.loads()

shelve.open()

yaml.load()

Use AST analysis to identify fully-qualified function calls.

Do not rely solely on string matching.

---

# Safe Patterns

Do NOT report:

yaml.safe_load()

or other explicitly safe deserialization APIs.

Only report APIs that are considered unsafe by default.

---

# Metadata

Provide appropriate rule metadata including:

- id
- name
- description
- severity
- confidence
- cwe
- owasp

Follow the same structure used by existing AST rules.

---

# Findings

For every detected API call, generate a finding containing information such as:

- rule id
- title
- description
- severity
- line number
- code snippet (if supported)
- CWE
- OWASP

Return findings through the existing framework.

Do not write directly to the database.

---

# Registry

Register the Unsafe Deserialization rule using the Rule Registry.

The AST engine should execute it automatically without requiring changes to ast_engine.py.

---

# Scope

This sprint detects usage of unsafe deserialization APIs only.

Do not perform:

- Taint analysis
- Trust boundary analysis
- User input tracking
- Runtime validation

Those belong to future enhancements.

---

# Do NOT

Do NOT implement

- Secret Detection
- Weak Crypto Detection
- Data Flow Analysis
- Taint Tracking

Do not modify BaseRule.

Do not modify the AST engine architecture.

---

# Files Allowed To Change

Primary

scanner/engines/ast/rules/deserialization.py

If required

scanner/engines/ast/registry.py

No unrelated files.

---

# Verification

Verify

✓ pickle.load() is detected

✓ pickle.loads() is detected

✓ dill.load() is detected

✓ dill.loads() is detected

✓ marshal.load() is detected

✓ marshal.loads() is detected

✓ yaml.load() is detected

✓ yaml.safe_load() is NOT reported

✓ Multiple unsafe deserialization calls generate multiple findings

✓ Safe code produces zero findings

✓ Existing scans continue working

✓ Django starts successfully

---

# Deliverables

The AST engine should successfully detect unsafe deserialization APIs and report findings through the existing framework.

No engine architecture changes should be introduced.

---

# Commit Message

feat(ast): add unsafe deserialization detection rule

---

# Stop

After verification

STOP.

Do not begin Secret Detection.