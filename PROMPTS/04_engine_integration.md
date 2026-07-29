# Phase 3 — Sprint 4

## AST Engine Refactor

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Refactor the existing AST engine so that it becomes an orchestrator rather than containing all future scanning logic.

The AST engine should coordinate the analysis process without embedding rule implementations.

This sprint focuses on architecture only.

Do NOT implement any vulnerability detection.

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

The registry and BaseRule have already been implemented.

No rule implementations currently exist.

---

# Objective

Refactor

scanner/engines/ast_engine.py

to become the central orchestrator.

The engine should be responsible for:

1. Reading Python source files.
2. Parsing source code into a Python AST.
3. Initializing the Rule Registry.
4. Executing every registered rule.
5. Collecting findings returned by the registry.
6. Returning findings in a consistent format.

The engine should not contain any detection logic.

---

# Desired Flow

The engine should approximately follow this sequence:

Read File

↓

Parse Python AST

↓

Initialize Registry

↓

Load Registered Rules

↓

Execute Rules

↓

Collect Findings

↓

Return Findings

Even when no rules are registered, the engine should execute successfully and return an empty collection.

---

# Responsibilities

The AST engine should only coordinate execution.

It should not:

- detect SQL Injection
- detect Command Injection
- detect Secrets
- detect Weak Crypto
- detect Dangerous Functions

Detection belongs exclusively to rule modules.

---

# Error Handling

The engine should gracefully handle:

- invalid Python syntax
- empty files
- missing files

Errors should not crash the scanning process.

Instead, return an appropriate empty result or controlled error according to the existing engine conventions.

---

# Design Principles

Maintain separation of responsibilities.

AST Engine

- orchestration
- parsing
- execution

Rule Registry

- manages rules

BaseRule

- defines rule contract

Rule Modules

- perform detection

Findings

- normalize output

No component should perform another component's responsibility.

---

# Do NOT

Do NOT implement

- Dangerous Function Detection
- SQL Injection Detection
- Command Injection Detection
- Secret Detection
- Weak Crypto Detection

Do NOT hardcode rule logic inside ast_engine.py.

Do NOT modify:

- bandit_engine.py
- semgrep_engine.py
- scanner/views.py
- scanner/models.py
- reports/
- templates/
- CSS
- JavaScript

---

# Files Allowed To Change

Only

scanner/engines/ast_engine.py

If absolutely necessary,

scanner/engines/ast/__init__.py

No other files.

---

# Verification

Verify

✓ Existing scans continue working

✓ Existing Bandit integration works

✓ Existing Semgrep integration works

✓ AST engine parses Python successfully

✓ Engine executes successfully with zero registered rules

✓ Empty findings are returned when no rules exist

✓ Django starts successfully

✓ No regressions

---

# Deliverables

At the end of this sprint the AST engine should be fully prepared for future rule implementations.

The engine should execute successfully even though no detection rules have been implemented.

---

# Commit Message

feat(ast): refactor engine into modular orchestrator

---

# Stop

After verification

STOP.

Do not implement any detection rules.

Do not begin Dangerous Function Detection.

Wait for the next sprint.