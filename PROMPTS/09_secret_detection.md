# Phase 3 — Sprint 9

## Hardcoded Secret Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement the fifth AST detection rule:

Hardcoded Secret Detection.

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
- Unsafe Deserialization Rule

This sprint extends the framework with one additional independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/secrets.py

The rule must inherit from BaseRule.

Follow the same coding style, metadata structure, and finding format used by the existing AST rules.

---

# Detection Scope

Detect assignments of hardcoded string literals to variables whose names strongly indicate credentials or secrets.

Examples include:

- password
- passwd
- pwd
- secret
- secret_key
- api_key
- apikey
- access_key
- access_token
- refresh_token
- token
- auth_token
- client_secret
- private_key
- aws_secret_access_key
- database_url

Detection should be based on Python AST.

Only report assignments where:

- the target variable name strongly indicates a secret
- the assigned value is a string literal (`ast.Constant` / string)

Examples:

```python
password = "admin123"

SECRET_KEY = "django-secret"

API_KEY = "abcd1234"

TOKEN = "eyJhbGciOi..."
```

---

# Ignore

Do NOT report values loaded from configuration or runtime sources.

Examples:

```python
password = os.getenv("PASSWORD")

SECRET_KEY = environ["SECRET_KEY"]

API_KEY = settings.API_KEY

DATABASE_URL = config["database_url"]
```

Also ignore:

- comments
- docstrings
- dictionary lookups
- function return values
- environment variables
- imported constants

---

# Detection Rules

This sprint detects only obvious hardcoded secrets.

Do NOT implement:

- entropy analysis
- regex-based token detection
- Git history scanning
- environment inspection
- API-specific token validation
- cloud provider key validation
- secret fingerprinting

Only inspect AST assignment nodes.

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

- CWE-798 (Use of Hard-coded Credentials)

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

scanner/engines/ast/rules/secrets.py

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

✓ Hardcoded password assignments are detected

✓ Hardcoded API keys are detected

✓ Hardcoded tokens are detected

✓ Hardcoded SECRET_KEY values are detected

✓ Hardcoded database_url assignments are detected

✓ os.getenv() values are NOT reported

✓ Environment-loaded values are NOT reported

✓ Imported configuration values are NOT reported

✓ Safe Python code generates zero findings

✓ Existing Dangerous Function detection still works

✓ Existing Command Injection detection still works

✓ Existing SQL Injection detection still works

✓ Existing Unsafe Deserialization detection still works

✓ Django starts successfully

✓ No regressions

---

# Deliverables

At the end of this sprint:

- One new independent Hardcoded Secret Detection rule exists.
- The rule integrates with the existing AST framework.
- No framework architecture has changed.
- Existing rules continue working unchanged.

---

# Commit Message

feat(ast): add hardcoded secret detection rule

---

# Stop

After verification

STOP.

Do not refactor the AST framework.

Do not modify existing rules.

Do not begin Weak Cryptography Detection.