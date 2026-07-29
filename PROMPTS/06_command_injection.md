# Phase 3 — Sprint 6

## Command Injection Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement a Command Injection detection rule for the ARGUS AST Framework.

This rule should identify Python code that executes operating system commands through common libraries and APIs.

The implementation must integrate with the existing AST framework.

Do not modify the engine architecture.

---

# Background

The AST framework is already complete.

Current components:

- AST Engine
- Rule Registry
- BaseRule
- Dangerous Functions Rule

This sprint adds a new independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/command_injection.py

Create a rule that inherits from BaseRule.

The rule should analyze Python AST nodes and detect potentially unsafe command execution APIs.

---

# Detect

Detect calls such as:

os.system()

os.popen()

subprocess.run()

subprocess.Popen()

subprocess.call()

subprocess.check_call()

subprocess.check_output()

Do not rely on string matching.

Use the parsed AST to identify fully-qualified function calls.

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

For every detected API call, generate a finding containing relevant information such as:

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

Register this rule using the Rule Registry.

The AST engine should execute it automatically without requiring changes to ast_engine.py.

---

# Scope

This sprint detects usage of command execution APIs only.

Do not attempt data-flow analysis.

Do not determine whether user input reaches the command.

Do not distinguish safe from unsafe arguments.

That level of analysis belongs to a future enhancement.

---

# Do NOT

Do NOT implement

- SQL Injection
- Secret Detection
- Weak Crypto Detection
- Unsafe Deserialization
- Taint Analysis
- User Input Tracking
- Data Flow Analysis

Do not modify BaseRule.

Do not modify the AST engine architecture.

---

# Files Allowed To Change

Primary

scanner/engines/ast/rules/command_injection.py

If required

scanner/engines/ast/registry.py

No unrelated files.

---

# Verification

Verify

✓ os.system() is detected

✓ os.popen() is detected

✓ subprocess.run() is detected

✓ subprocess.Popen() is detected

✓ subprocess.call() is detected

✓ subprocess.check_call() is detected

✓ subprocess.check_output() is detected

✓ Multiple command execution calls produce multiple findings

✓ Safe Python code produces zero findings

✓ Existing scans continue working

✓ Django starts successfully

---

# Deliverables

The AST engine should successfully detect common command execution APIs and report findings through the existing framework.

This sprint should introduce no changes to the overall engine architecture.

---

# Commit Message

feat(ast): add command injection detection rule

---

# Stop

After verification

STOP.

Do not begin SQL Injection detection.