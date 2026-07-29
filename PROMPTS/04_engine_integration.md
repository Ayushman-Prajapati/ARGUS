# Phase 3 — Sprint 4

## AST Engine Refactor

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Refactor the existing AST engine so that it becomes a lightweight orchestrator.

The AST engine should coordinate the analysis process without containing any vulnerability detection logic.

This sprint is architecture only.

Do NOT implement any detection rules.

---

# Background

The following components already exist.

scanner/
└── engines/
    ├── ast_engine.py
    └── ast/
        ├── registry.py
        ├── base_rule.py
        ├── findings.py
        ├── utils.py
        └── rules/

The Rule Registry and BaseRule have already been implemented.

The rule modules currently exist only as empty placeholders.

---

# Objective

Refactor

scanner/engines/ast_engine.py

into a pure orchestrator.

Its responsibilities are limited to:

1. Parse Python source into an AST.
2. Create a RuleRegistry instance.
3. Register available rules.
4. Execute all registered rules.
5. Collect findings.
6. Return findings.

The engine must not contain any vulnerability-specific logic.

---

# Execution Flow

The engine should approximately follow this sequence.

Read Source

↓

Parse Python AST

↓

Create RuleRegistry

↓

Register Rules

↓

Execute Rules

↓

Collect Findings

↓

Return Findings

If no rules are registered, the engine should return an empty collection without errors.

---

# Rule Execution Contract

Use the existing BaseRule interface.

Every rule is executed through

```python
rule.visit(tree)
```

The Rule Registry should execute rules using **visit(tree)**.

Do NOT introduce:

- check()
- execute()
- run()

Do NOT add compatibility wrappers.

The BaseRule interface must remain unchanged.

---

# Rule Registration

For this sprint, register rules explicitly.

Do NOT implement:

- automatic rule discovery
- plugin loading
- dynamic imports
- reflection-based registration

Those belong to a future enhancement.

---

# Responsibilities

AST Engine

- parsing
- orchestration
- execution
- error handling

Rule Registry

- stores rule instances
- executes rule.visit(tree)
- aggregates findings

BaseRule

- defines the rule interface

Rule Modules

- perform vulnerability detection

Findings

- normalize rule output

Every component must have a single responsibility.

---

# Error Handling

Handle gracefully:

- invalid Python syntax
- empty files
- missing files

The engine must never crash because of malformed input.

Return an empty collection or a controlled error consistent with the existing engine behavior.

---

# Do NOT

Do NOT implement:

- Dangerous Function Detection
- Command Injection Detection
- SQL Injection Detection
- Secret Detection
- Weak Crypto Detection
- Unsafe Deserialization Detection

Do NOT hardcode any detection logic inside ast_engine.py.

Do NOT change:

- BaseRule
- RuleRegistry public API
- scanner/views.py
- scanner/models.py
- bandit_engine.py
- semgrep_engine.py
- reports/
- templates/
- CSS
- JavaScript

---

# Files Allowed To Change

Only

scanner/engines/ast_engine.py

Optionally

scanner/engines/ast/__init__.py

No other files.

---

# Verification

Verify:

✓ Django starts successfully

✓ Existing Bandit engine works

✓ Existing Semgrep engine works

✓ Python source parses successfully

✓ Engine executes with zero registered rules

✓ Empty findings are returned when no rules exist

✓ Existing scan workflow remains unchanged

✓ No regressions are introduced

---

# Deliverables

At the end of this sprint:

- ast_engine.py is a lightweight orchestrator.
- Rule execution is delegated entirely to RuleRegistry.
- Rules are executed using BaseRule.visit(tree).
- No vulnerability detection exists inside ast_engine.py.
- The engine successfully returns an empty finding list when no rules are registered.

---

# Commit Message

feat(ast): refactor AST engine into orchestrator

---

# Stop

After verification:

STOP.

Do not implement any detection rules.

Do not modify BaseRule or RuleRegistry.

Do not implement automatic rule discovery.

Wait for the next sprint.