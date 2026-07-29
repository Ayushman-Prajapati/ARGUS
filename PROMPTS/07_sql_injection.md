# Phase 3 — Sprint 7

## SQL Injection Detection

Follow the instructions in `.claude.md` before reading this prompt.

---

# Objective

Implement a SQL Injection detection rule for the ARGUS AST Framework.

This rule should identify Python code that constructs and executes SQL queries using potentially unsafe patterns.

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

This sprint introduces a new independent rule for SQL Injection detection.

---

# Implement

Implement

scanner/engines/ast/rules/sql_injection.py

Create a rule that inherits from BaseRule.

The rule should analyze Python AST nodes and detect unsafe SQL query construction patterns.

---

# Detect

Detect common SQL execution APIs such as:

cursor.execute()

cursor.executemany()

connection.execute()

session.execute()

and identify unsafe query construction patterns including:

- String concatenation
- "%" string formatting
- str.format()
- f-strings used to build SQL
- Other dynamically constructed SQL strings

Use AST analysis to inspect how the SQL query argument is built.

Do not rely on plain text or regular expression matching.

---

# Safe Patterns

Do not report parameterized queries, including examples such as:

cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (user_id,)
)

or equivalent parameterized APIs supported by common Python database libraries.

The focus is on identifying unsafe query construction rather than all SQL execution.

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

Use the same format as existing AST rules.

---

# Findings

For each detected issue, generate a finding containing information such as:

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

Register the SQL Injection rule using the Rule Registry.

The AST engine should execute it automatically without requiring modifications to ast_engine.py.

---

# Scope

This sprint is limited to syntax-based SQL Injection detection.

Do not perform:

- Taint analysis
- User input tracking
- Variable propagation
- Interprocedural analysis
- Database-specific query validation

Those belong to future enhancements.

---

# Do NOT

Do NOT implement

- Secret Detection
- Weak Crypto Detection
- Unsafe Deserialization
- Data Flow Analysis
- Taint Tracking

Do not modify BaseRule.

Do not modify the AST engine architecture.

---

# Files Allowed To Change

Primary

scanner/engines/ast/rules/sql_injection.py

If required

scanner/engines/ast/registry.py

No unrelated files.

---

# Verification

Verify

✓ String concatenation used in SQL is detected

✓ f-string SQL queries are detected

✓ str.format() SQL queries are detected

✓ "%" formatted SQL queries are detected

✓ Parameterized queries are not reported

✓ Multiple SQL issues generate multiple findings

✓ Safe code produces zero findings

✓ Existing scans continue working

✓ Django starts successfully

---

# Deliverables

The AST engine should successfully detect common unsafe SQL query construction patterns and report findings through the existing framework.

No engine architecture changes should be introduced.

---

# Commit Message

feat(ast): add SQL injection detection rule

---

# Stop

After verification

STOP.

Do not begin Unsafe Deserialization detection.