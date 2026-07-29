# ARGUS - CURRENT SPRINT

Status

🚧 Active Development

Current Version

v0.2.0

Current Phase

Phase 3 — Custom AST Engine

Current Branch

feature/ast-engine

---

# Sprint Goal

Build the foundation of the ARGUS AST Engine.

This sprint focuses ONLY on the AST engine architecture.

Objectives

- Design a modular AST analysis framework.
- Build an extensible rule execution system.
- Integrate AST findings with the existing Finding model.
- Preserve compatibility with Bandit and Semgrep.

No UI redesigns.

No CSS changes.

No JavaScript changes.

No dashboard improvements.

No authentication changes.

No report redesign.

---

# Sprint Rules

One sprint at a time.

Each completed sprint must be

- Implemented
- Tested
- Reviewed
- Committed
- Verified

before beginning the next sprint.

One prompt = One sprint = One commit.

---

# Sprint 1 — AST Engine Architecture

Status

⬜ Pending

Requirements

Create the AST engine foundation.

Implement

- AST Parser
- Engine Entry Point
- Rule Registry
- Base Rule
- Finding Generator
- Rule Loader

Architecture should support adding future rules without modifying the engine.

Files (expected)

scanner/scanners/ast_engine/

---

# Sprint 2 — Dangerous Function Detection

Status

⬜ Pending

Detect

- eval()
- exec()
- compile()
- globals()
- locals()

Each finding should include

- Severity
- Confidence
- CWE
- OWASP
- Evidence
- Remediation

---

# Sprint 3 — Command Injection

Status

⬜ Pending

Detect

- os.system()
- os.popen()
- subprocess.run(shell=True)
- subprocess.Popen(shell=True)
- subprocess.call(shell=True)

---

# Sprint 4 — SQL Injection

Status

⬜ Pending

Detect insecure SQL execution

Examples

- execute(f"...")
- execute("%s" % ...)
- execute("..." + user_input)
- .format()

---

# Sprint 5 — Unsafe Deserialization

Status

⬜ Pending

Detect

- pickle.loads()
- yaml.load()
- marshal.loads()
- dill.loads()

---

# Sprint 6 — Secret Detection

Status

⬜ Pending

Detect

- Hardcoded Passwords
- AWS Keys
- GitHub Tokens
- JWT Secrets
- API Keys
- Private Keys

---

# Sprint 7 — Weak Cryptography

Status

⬜ Pending

Detect

- MD5
- SHA1
- DES
- ECB Mode
- Weak Random
- Predictable Tokens

---

# Sprint 8 — Optimization & Testing

Status

⬜ Pending

Requirements

- Improve performance
- Reduce duplicate traversals
- Optimize rule execution
- Documentation
- Unit Tests
- Integration Tests

---

# Out of Scope

Do NOT modify

- Dashboard
- Scan Detail UI
- Homepage
- CSS
- JavaScript
- Authentication
- Reports
- REST API
- Docker
- Repository Explorer
- AI Features

Unless explicitly requested.

---

# Testing Checklist

Every completed sprint must satisfy

☐ Django starts successfully

☐ No Python errors

☐ Existing scans still work

☐ Existing reports still generate

☐ Existing dashboard remains functional

☐ Bandit integration still works

☐ Semgrep integration still works

☐ AST findings integrate correctly

☐ No performance regressions

☐ Code follows PEP 8

---

# Commit Strategy

One sprint = One commit

Examples

feat(ast): create engine architecture

feat(ast): implement rule registry

feat(ast): detect dangerous functions

feat(ast): detect command injection

feat(ast): detect SQL injection

feat(ast): detect unsafe deserialization

feat(ast): implement secret detection

feat(ast): implement weak crypto detection

feat(ast): optimize engine

Never combine multiple unrelated sprints into a single commit.

---

# Claude Instructions

Before editing

1. Inspect the existing implementation.
2. Explain the implementation strategy.
3. List every file that will be modified.
4. Wait for approval if more than two files require modification.

After editing

1. Verify Django starts successfully.
2. Verify existing scans still work.
3. Verify Bandit integration.
4. Verify Semgrep integration.
5. Verify AST engine integration.
6. Stop.

Never automatically continue to the next sprint.

Wait for the next prompt.