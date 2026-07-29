# Phase 3 — Sprint 9

## Secret Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement a Secret Detection rule for the ARGUS AST Framework.

This rule should identify hardcoded secrets and credentials embedded directly in Python source code.

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
- Unsafe Deserialization Rule

This sprint introduces a new independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/secrets.py

Create a rule that inherits from BaseRule.

The rule should analyze Python AST nodes and detect hardcoded secrets.

---

# Detect

Detect assignments of hardcoded values to variables whose names strongly indicate credentials or secrets.

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

Detect values assigned as string literals.

Examples:

password = "admin123"

SECRET_KEY = "django-secret"

API_KEY = "abcd1234"

TOKEN = "eyJhbGciOi..."

---

# High Confidence Only

Only report assignments where:

- the variable name strongly suggests a credential
- the assigned value is a string literal

Do NOT attempt entropy analysis.

Do NOT detect secrets inside comments.

Do NOT scan text files.

Do NOT inspect environment variables.

---

# Ignore

Do NOT report:

password = os.getenv("PASSWORD")

SECRET_KEY = environ["SECRET_KEY"]

config["api_key"]

Values loaded from external configuration.

The rule is only concerned with hardcoded literals.

---

# Metadata

Provide metadata including:

- id
- name
- description
- severity
- confidence
- cwe
- owasp

Use the same structure as existing AST rules.

---

# Findings

For each detected secret generate a finding containing:

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

Register the Secret Detection rule using the Rule Registry.

The AST engine should execute it automatically.

Do not modify ast_engine.py.

---

# Scope

This sprint is limited to detecting hardcoded secrets in Python source code.

Do not implement:

- Entropy analysis
- Regex-based secret scanning
- Git history scanning
- Environment inspection
- Secret validation
- API-specific token recognition

Those belong to future enhancements.

---

# Do NOT

Do NOT modify

- BaseRule
- AST Engine
- Existing detection rules

Do not implement Weak Crypto Detection.

---

# Files Allowed To Change

Primary

scanner/engines/ast/rules/secrets.py

If required

scanner/engines/ast/registry.py

No unrelated files.

---

# Verification

Verify

✓ Hardcoded password assignments are detected

✓ Hardcoded API keys are detected

✓ Hardcoded tokens are detected

✓ Hardcoded SECRET_KEY values are detected

✓ os.getenv() values are NOT reported

✓ Environment-loaded values are NOT reported

✓ Safe code produces zero findings

✓ Existing scans continue working

✓ Django starts successfully

---

# Deliverables

The AST engine should successfully detect hardcoded credentials and secrets using AST analysis while avoiding configuration-based values.

No engine architecture changes should be introduced.

---

# Commit Message

feat(ast): add hardcoded secret detection rule

---

# Stop

After verification

STOP.

Do not begin Weak Crypto Detection.