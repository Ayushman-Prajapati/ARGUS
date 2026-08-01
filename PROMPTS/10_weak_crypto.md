# Phase 3 — Sprint 10

## Weak Cryptography Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement the sixth AST detection rule:

Weak Cryptography Detection.

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
- Hardcoded Secret Detection Rule

This sprint extends the framework with one additional independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/weak_crypto.py

The rule must inherit from BaseRule.

Follow the same coding style, metadata structure, and finding format used by the existing AST rules.

---

# Detection Scope

Detect usage of weak cryptographic primitives using Python AST.

## Weak Hash Algorithms

Detect:

- hashlib.md5()
- hashlib.sha1()

Do NOT report:

- hashlib.sha256()
- hashlib.sha384()
- hashlib.sha512()
- hashlib.sha3_256()
- hashlib.sha3_512()
- hashlib.blake2b()
- hashlib.blake2s()

---

## Weak Cipher Algorithms

Detect:

- Crypto.Cipher.DES
- Crypto.Cipher.ARC4
- Crypto.Cipher.Blowfish

Detect equivalent imported aliases where possible.

Also detect:

- cryptography.hazmat.primitives.ciphers.algorithms.DES
- cryptography.hazmat.primitives.ciphers.algorithms.ARC4

---

## Insecure Cipher Modes

Detect:

- ECB mode

Examples include:

- AES.MODE_ECB
- modes.ECB()

---

# Ignore

Do NOT report:

- AES-GCM
- AES-CBC
- ChaCha20
- AES-CTR
- Fernet

This sprint detects only algorithms and modes that are widely considered insecure.

---

# Detection Rules

Use AST node analysis.

Resolve imports and aliases in the same manner as the existing Command Injection and Unsafe Deserialization rules.

Do NOT use:

- regular expressions
- plain text searching
- string matching alone

---

# Scope

This sprint detects usage of weak cryptographic primitives only.

Do NOT implement:

- cryptographic misuse analysis
- random number analysis
- TLS configuration analysis
- certificate validation
- key length validation
- entropy analysis
- padding validation
- IV reuse detection

Those belong to future enhancements.

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

- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm)

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

scanner/engines/ast/rules/weak_crypto.py

If required by the existing registration mechanism

scanner/engines/ast/__init__.py

scanner/engines/ast/rules/__init__.py

No other files.

Specifically do NOT modify:

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

✓ hashlib.md5() is detected

✓ hashlib.sha1() is detected

✓ Crypto.Cipher.DES is detected

✓ Crypto.Cipher.ARC4 is detected

✓ Crypto.Cipher.Blowfish is detected

✓ algorithms.DES is detected

✓ algorithms.ARC4 is detected

✓ AES.MODE_ECB is detected

✓ modes.ECB() is detected

✓ hashlib.sha256() is NOT reported

✓ hashlib.sha512() is NOT reported

✓ AES-GCM is NOT reported

✓ AES-CBC is NOT reported

✓ Safe cryptographic usage generates zero findings

✓ Existing Dangerous Function detection still works

✓ Existing Command Injection detection still works

✓ Existing SQL Injection detection still works

✓ Existing Unsafe Deserialization detection still works

✓ Existing Hardcoded Secret detection still works

✓ Django starts successfully

✓ No regressions

---

# Deliverables

At the end of this sprint:

- One new independent Weak Cryptography Detection rule exists.
- The rule integrates with the existing AST framework.
- No framework architecture has changed.
- Existing rules continue working unchanged.

---

# Commit Message

feat(ast): add weak cryptography detection rule

---

# Stop

After verification

STOP.

Do not refactor the AST framework.

Do not modify existing rules.

Phase 3 rule implementation is complete.