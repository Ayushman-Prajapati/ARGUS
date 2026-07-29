# Phase 3 — Sprint 5

## Dangerous Function Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement the first AST detection rule for the ARGUS AST Framework.

This rule should detect calls to dangerous built-in Python functions.

This sprint validates that the entire AST framework works correctly from:

AST Engine

↓

Rule Registry

↓

Rule Execution

↓

Findings Collection

No other detection rules should be implemented.

---

# Background

The AST framework has already been completed.

Current architecture:

scanner/
└── engines/
    ├── ast_engine.py
    └── ast/
        ├── registry.py
        ├── base_rule.py
        ├── findings.py
        ├── utils.py
        └── rules/
            └── dangerous_functions.py

The engine should already execute registered rules successfully.

---

# Implement

Implement

scanner/engines/ast/rules/dangerous_functions.py

This module should define a rule that inherits from BaseRule.

The rule should analyze the Python AST and identify calls to dangerous built-in functions.

---

# Functions To Detect

Detect calls to:

- eval()
- exec()
- compile()

Only direct function calls.

Examples:

eval(user_input)

exec(code)

compile(source, filename, mode)

Do not detect similarly named variables or strings.

---

# Metadata

Provide appropriate metadata including:

- id
- name
- description
- severity
- confidence
- cwe
- owasp

Use values consistent with the project's existing finding format.

---

# Findings

For each detected function call, return a finding containing relevant information such as:

- rule id
- title
- description
- severity
- line number
- code snippet (if supported)
- CWE
- OWASP

Do not save findings directly to the database.

Return them to the engine through the existing framework.

---

# Registry

Register the Dangerous Function rule using the Rule Registry.

Do not hardcode execution inside ast_engine.py.

The engine should execute the rule automatically through the registry.

---

# Do NOT

Do NOT implement

- SQL Injection
- Command Injection
- Secret Detection
- Weak Crypto
- Deserialization Detection

Do not modify the engine architecture.

Do not modify BaseRule.

Do not modify the registry unless required to register the new rule.

---

# Files Allowed To Change

Primary:

scanner/engines/ast/rules/dangerous_functions.py

If required:

scanner/engines/ast/registry.py

No unrelated files.

---

# Verification

Verify

✓ eval() is detected

✓ exec() is detected

✓ compile() is detected

✓ Multiple dangerous calls are reported

✓ Safe Python code produces zero findings

✓ Existing scans continue working

✓ Django starts successfully

---

# Deliverables

The AST engine should successfully execute its first detection rule and return findings for dangerous built-in function usage.

No other vulnerability categories should be implemented.

---

# Commit Message

feat(ast): add dangerous function detection rule

---

# Stop

After verification

STOP.

Do not begin Command Injection detection.