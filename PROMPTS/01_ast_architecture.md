# Phase 3 — Sprint 1

## AST Framework Architecture

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Create the foundational folder structure for the ARGUS AST Framework.

This sprint is **architecture only**.

Do not implement any detection logic.

Do not refactor existing code.

Do not modify the scan pipeline.

---

# Existing Structure

The following files already exist.

scanner/
└── engines/
    ├── __init__.py
    ├── ast_engine.py
    ├── bandit_engine.py
    └── semgrep_engine.py

Do NOT modify them.

---

# Create Only

Create the following structure.

scanner/
└── engines/
    └── ast/
        ├── __init__.py
        ├── registry.py
        ├── base_rule.py
        ├── findings.py
        ├── utils.py
        └── rules/
            ├── __init__.py
            ├── dangerous_functions.py
            ├── command_injection.py
            ├── sql_injection.py
            ├── deserialization.py
            ├── secrets.py
            └── weak_crypto.py

If any of these files already exist, leave them unchanged.

---

# Requirements

Each newly created file should contain only:

- a module docstring describing its future purpose
- no implementation
- no classes
- no functions
- no detection logic
- no placeholder algorithms

The purpose of this sprint is only to establish the project structure.

---

# Do NOT

Do NOT implement

- Rule Registry
- BaseRule
- AST Traversal
- Rule Discovery
- SQL Injection Detection
- Command Injection Detection
- Secret Detection
- Weak Cryptography Detection
- Finding Generation
- Engine Integration

These belong to later sprints.

---

# Files Allowed To Change

Only create the files inside

scanner/engines/ast/

No other files may be modified.

---

# Verification

Verify

- Django starts successfully
- No import errors
- Existing Bandit engine is unaffected
- Existing Semgrep engine is unaffected
- Existing AST engine is unchanged

---

# Deliverables

At the end of this sprint the repository should contain the complete AST framework folder structure ready for implementation in future sprints.

No functionality should change.

---

# Commit Message

feat(ast): create AST framework structure

---

# Stop

After verification, stop.

Do not continue to the next sprint.