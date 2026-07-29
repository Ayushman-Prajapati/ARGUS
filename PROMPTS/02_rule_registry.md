# Phase 3 — Sprint 2

## AST Rule Registry

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement a modular Rule Registry for the ARGUS AST Engine.

The registry will become the central location responsible for managing AST rules.

This sprint should ONLY implement the registry.

Do NOT implement any detection rules.

Do NOT modify ast_engine.py.

---

# Background

The AST framework folder already exists.

scanner/
└── engines/
    └── ast/
        ├── registry.py
        ├── base_rule.py
        ├── findings.py
        ├── utils.py
        └── rules/

This sprint focuses only on `registry.py`.

---

# Responsibilities

Implement a registry capable of:

- Registering rules
- Unregistering rules
- Listing registered rules
- Executing all registered rules

The registry should be generic and reusable.

Future rule implementations should require only registration, without modifying the registry itself.

---

# Public API

The registry should expose functionality equivalent to:

- register(rule)
- unregister(rule)
- list_rules()
- execute_all(tree)

Do not expose unnecessary public methods.

Use clean, object-oriented design.

---

# Execution Behavior

The registry should:

1. Maintain an internal collection of rule instances.
2. Execute every registered rule in order.
3. Collect results from each rule.
4. Return a single combined collection of findings.

No rule should know about any other rule.

The registry must remain independent of the scanning engine.

---

# Current Limitation

There are currently no implemented rules.

The registry should therefore execute successfully even when no rules exist.

Expected behavior:

- No exceptions
- Empty collection returned
- Clean execution

---

# Do NOT

Do NOT modify

- ast_engine.py
- bandit_engine.py
- semgrep_engine.py
- base_rule.py
- findings.py
- utils.py

Do NOT create

- SQL Injection detection
- Command Injection detection
- Secret detection
- Weak crypto detection
- AST traversal
- Rule discovery
- Rule loading

Those belong to future sprints.

---

# Files Allowed To Change

Only

scanner/engines/ast/registry.py

No other files.

---

# Verification

Verify

✓ Registry can register a rule

✓ Registry can unregister a rule

✓ Registry can list registered rules

✓ Registry executes successfully with zero rules

✓ Registry returns an empty collection when no rules exist

✓ Django starts successfully

✓ Existing scan functionality remains unchanged

---

# Deliverables

A reusable Rule Registry ready for future AST rules.

No vulnerability detection should exist after this sprint.

---

# Commit Message

feat(ast): implement modular rule registry

---

# Stop

After verification, stop.

Do not implement BaseRule.

Do not modify ast_engine.py.

Do not continue to the next sprint.