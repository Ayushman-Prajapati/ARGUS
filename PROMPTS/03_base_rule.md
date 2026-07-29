# Phase 3 — Sprint 3

## Base Rule Architecture

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement the Base Rule abstraction for the ARGUS AST Framework.

Every future AST detection rule must inherit from this class.

The goal is to standardize how rules describe themselves and how they return findings.

This sprint is architecture only.

Do NOT implement any vulnerability detection.

---

# Background

The AST framework now contains

scanner/
└── engines/
    └── ast/
        ├── registry.py
        ├── base_rule.py
        ├── findings.py
        ├── utils.py
        └── rules/

The registry already exists.

This sprint implements only the Base Rule.

---

# Responsibilities

Implement a reusable abstract BaseRule class.

Every future rule should inherit from it.

The BaseRule should define a consistent interface for all AST rules.

---

# Rule Metadata

Every rule should expose metadata including

- id
- name
- description
- severity
- confidence
- cwe
- owasp

Use appropriate defaults where applicable.

---

# Required Interface

Every rule should implement a method similar to

```python
visit(tree)
```

The base class should define this interface but should not implement any detection logic.

---

# Findings

The BaseRule should not save findings.

The BaseRule should not know anything about Django models.

It should only define the contract that subclasses must follow.

Finding persistence belongs to the engine.

---

# Design Requirements

Use Python's abstract base class (`abc.ABC`) or an equivalent abstract interface.

The BaseRule should:

- enforce required methods
- encourage consistent metadata
- remain independent of Django
- remain independent of the registry
- remain independent of ast_engine.py

Future rules should only need to inherit BaseRule and implement their own logic.

---

# Do NOT

Do NOT implement

- SQL Injection detection
- Command Injection detection
- Secret detection
- Weak Crypto detection
- Rule loading
- Rule discovery
- AST traversal
- Finding persistence
- Engine integration

Those belong to future sprints.

---

# Files Allowed To Change

Only

scanner/engines/ast/base_rule.py

No other files.

---

# Verification

Verify

✓ BaseRule can be imported

✓ BaseRule cannot be instantiated directly (if abstract)

✓ Future subclasses can inherit from BaseRule

✓ Registry compatibility is preserved

✓ Django starts successfully

✓ Existing scan functionality remains unchanged

---

# Deliverables

A reusable abstract BaseRule class that will become the foundation for every future AST detection rule.

No vulnerability detection should exist after this sprint.

---

# Commit Message

feat(ast): implement abstract base rule

---

# Stop

After verification

STOP.

Do not modify ast_engine.py.

Do not implement detection rules.

Do not continue to the next sprint.