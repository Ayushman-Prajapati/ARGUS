# Phase 3 — Sprint 10

## Weak Cryptography Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement a Weak Cryptography detection rule for the ARGUS AST Framework.

This rule should identify the use of insecure cryptographic algorithms, weak hashing functions, and outdated cipher modes.

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
- Secret Detection Rule

This sprint introduces a new independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/weak_crypto.py

Create a rule that inherits from BaseRule.

The rule should analyze Python AST nodes and detect insecure cryptographic usage.

---

# Detect

Detect usage of weak hashing algorithms including:

- hashlib.md5()
- hashlib.sha1()

Detect cryptographic library usage including:

- Crypto.Cipher.DES
- Crypto.Cipher.ARC4
- Crypto.Cipher.Blowfish
- algorithms.DES
- algorithms.ARC4

Detect insecure cipher modes where applicable:

- ECB mode

Use AST analysis to identify imported modules and fully-qualified function or class usage.

Do not rely solely on string matching.

---

# Ignore

Do NOT report secure algorithms such as:

- hashlib.sha256()
- hashlib.sha384()
- hashlib.sha512()
- hashlib.blake2b()
- hashlib.blake2s()
- hashlib.sha3_256()
- AES with secure modes such as GCM or CBC (unless another rule specifically addresses misuse)

Only report algorithms widely considered insecure.

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

For every detected issue generate a finding containing:

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

Register the Weak Cryptography rule using the Rule Registry.

The AST engine should execute it automatically.

Do not modify ast_engine.py.

---

# Scope

This sprint is limited to detecting known weak cryptographic primitives.

Do not implement:

- Cryptographic misuse analysis
- Random number quality analysis
- TLS configuration analysis
- Certificate validation
- Key length validation
- Entropy analysis

Those belong to future enhancements.

---

# Do NOT

Do NOT modify

- BaseRule
- AST Engine
- Existing detection rules

---

# Files Allowed To Change

Primary

scanner/engines/ast/rules/weak_crypto.py

If required

scanner/engines/ast/registry.py

No unrelated files.

---

# Verification

Verify

✓ hashlib.md5() is detected

✓ hashlib.sha1() is detected

✓ DES usage is detected

✓ ARC4 usage is detected

✓ Blowfish usage is detected

✓ ECB mode is detected

✓ hashlib.sha256() is NOT reported

✓ hashlib.sha512() is NOT reported

✓ Safe cryptographic usage produces zero findings

✓ Existing scans continue working

✓ Django starts successfully

---

# Deliverables

The AST engine should successfully detect common weak cryptographic algorithms and insecure cipher usage while avoiding modern secure algorithms.

No engine architecture changes should be introduced.

---

# Commit Message

feat(ast): add weak cryptography detection rule

---

# Stop

After verification

STOP.

Do not begin new detection categories.