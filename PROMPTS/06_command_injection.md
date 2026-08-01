# Phase 3 — Sprint 6

## Command Injection Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement the second AST detection rule:

Command Injection Detection.

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

This sprint extends the framework by introducing one additional rule.

---

# Implement

Implement

scanner/engines/ast/rules/command_injection.py

The rule must inherit from BaseRule.

Follow the same implementation style, metadata structure, and finding format used by DangerousFunctionRule.

---

# Detection Scope

Detect direct calls to the following command execution APIs using the parsed AST.

## os module

- os.system()
- os.popen()

## subprocess module

- subprocess.run()
- subprocess.Popen()
- subprocess.call()
- subprocess.check_call()
- subprocess.check_output()

Use AST node analysis.

Do not rely on string searching.

Only detect fully-qualified function calls.

---

# Detection Rules

Report usage whenever one of the supported APIs is called.

This sprint detects API usage only.

Do NOT attempt to determine whether user input reaches the command.

Do NOT perform:

- taint analysis
- data-flow analysis
- symbolic execution
- argument validation

Those belong to future sprints.

---

# Metadata

Provide metadata consistent with existing AST rules.

Include

- id
- name
- description
- severity
- confidence
- cwe
- owasp

Use the same style as DangerousFunctionRule.

---

# Findings

Return findings using the existing normalized format.

Each finding should include

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

Register the rule using the **existing registration mechanism**.

Do not redesign or replace the current registration process.

Do not modify the AST engine.

---

# Files Allowed To Change

Primary

scanner/engines/ast/rules/command_injection.py

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

Verify

✓ os.system()

✓ os.popen()

✓ subprocess.run()

✓ subprocess.Popen()

✓ subprocess.call()

✓ subprocess.check_call()

✓ subprocess.check_output()

✓ Multiple command execution APIs generate multiple findings

✓ Safe Python code generates zero findings

✓ Existing Dangerous Function detection still works

✓ Existing scans continue working

✓ Django starts successfully

✓ No regressions

---

# Deliverables

At the end of this sprint

- One new independent AST rule exists.
- The rule integrates with the existing framework.
- No framework architecture has changed.
- No unrelated files have been modified.

---

# Commit Message

feat(ast): add command injection detection rule

---

# Stop

After verification

STOP.

Do not refactor the AST framework.

Do not improve existing rules.

Do not begin SQL Injection Detection.