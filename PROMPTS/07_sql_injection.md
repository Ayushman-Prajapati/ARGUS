# Phase 3 — Sprint 7

## SQL Injection Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement the third AST detection rule:

SQL Injection Detection.

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

This sprint extends the framework with one additional independent rule.

---

# Implement

Implement

scanner/engines/ast/rules/sql_injection.py

The rule must inherit from BaseRule.

Follow the same coding style, metadata structure, and finding format used by the existing AST rules.

---

# Detection Scope

Detect SQL execution through common database APIs.

Supported execution methods include:

- cursor.execute(...)
- cursor.executemany(...)
- connection.execute(...)
- session.execute(...)

Detect unsafe SQL query construction patterns including:

- String concatenation (+)
- Percent (%) string formatting
- str.format()
- f-strings
- Dynamically constructed SQL strings passed directly into execution APIs

Use Python AST analysis.

Do not use:

- regular expressions
- plain text searching
- string matching alone

---

# Safe Patterns

Do NOT report parameterized queries.

Examples that should NOT produce findings:

```python
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (user_id,)
)

cursor.execute(
    "SELECT * FROM users WHERE id = ?",
    (user_id,)
)
```

Equivalent parameterized APIs should also be treated as safe.

---

# Detection Rules

This sprint performs syntax-based detection only.

Do NOT implement:

- taint analysis
- user-input tracking
- variable propagation
- alias propagation
- interprocedural analysis
- symbolic execution
- ORM-specific analysis

Only inspect the AST of the SQL expression supplied to supported execution methods.

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

Use CWE-89 and the appropriate OWASP category.

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

scanner/engines/ast/rules/sql_injection.py

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

✓ String concatenation SQL queries are detected

✓ f-string SQL queries are detected

✓ str.format() SQL queries are detected

✓ Percent-formatted SQL queries are detected

✓ Parameterized queries are NOT reported

✓ Multiple SQL Injection issues generate multiple findings

✓ Safe Python code generates zero findings

✓ Existing Dangerous Function detection still works

✓ Existing Command Injection detection still works

✓ Django starts successfully

✓ No regressions

---

# Deliverables

At the end of this sprint:

- One new independent SQL Injection rule exists.
- The rule integrates with the existing AST framework.
- No framework architecture has changed.
- Existing rules continue working unchanged.

---

# Commit Message

feat(ast): add SQL injection detection rule

---

# Stop

After verification

STOP.

Do not refactor the AST framework.

Do not modify existing rules.

Do not begin Unsafe Deserialization Detection.