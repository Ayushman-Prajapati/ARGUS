# ARGUS — CURRENT SPRINT

Status

🚧 Active Development

Current Version

**v0.4.0**

Current Phase

**Phase 5 — Scan Experience**

Current Branch

`feature/scan-experience`

---

# Phase Goal

Transform the scanning workflow into a modern, interactive experience that provides continuous feedback while preserving the existing backend architecture.

This phase focuses on improving the user experience during scans without changing the security analysis engines.

Objectives

- Live scan progress
- Engine-by-engine progress
- Improved scan lifecycle
- Better re-scan behavior
- Interactive demo scan
- Live scan console
- User notifications
- Scan comparison
- Improved scan history

No scanner logic changes.

No AST rule changes.

No authentication changes.

No database schema changes unless explicitly required.

---

# Sprint Rules

One sprint at a time.

Every completed sprint must be:

- Implemented
- Reviewed
- Tested
- Committed
- Verified

One prompt = One sprint = One commit.

---

# Sprint 1 — Live Scan Progress

Status

⬜ Pending

Objectives

- Progress Bar
- Progress Percentage
- Loading States
- Estimated Progress
- Prevent page reload feeling

Primary Areas

- Scan creation workflow
- Progress UI

---

# Sprint 2 — Engine Progress

Status

⬜ Pending

Objectives

- Bandit status
- Semgrep status
- Safety status
- pip-audit status
- ARGUS AST status

Display

- Pending
- Running
- Completed
- Failed

---

# Sprint 3 — Scan Lifecycle

Status

⬜ Pending

Objectives

- Running state
- Success state
- Failure state
- Better loading flow
- Improved completion handling

---

# Sprint 4 — Re-scan Experience

Status

⬜ Pending

Objectives

- Update scan timestamp
- Refresh scan duration
- Improve scan history
- Prevent duplicate submissions
- Better success feedback

---

# Sprint 5 — Demo Scan Experience

Status

⬜ Pending

Objectives

- Interactive demo scan
- Simulated engine execution
- Animated progress
- Better onboarding

---

# Sprint 6 — Live Scan Console

Status

⬜ Pending

Objectives

- Live log output
- Engine messages
- Scan timeline
- Status updates

---

# Sprint 7 — Notifications

Status

⬜ Pending

Objectives

- Success notifications
- Error notifications
- Warning notifications
- Toast messages

---

# Sprint 8 — Scan History

Status

⬜ Pending

Objectives

- Better scan history
- Previous scan visibility
- Latest scan highlighting
- Improved timeline

---

# Sprint 9 — Scan Comparison

Status

⬜ Pending

Objectives

- Risk comparison
- Finding comparison
- Severity delta
- Historical trends

---

# Sprint 10 — Testing & Cleanup

Status

⬜ Pending

Objectives

- Performance review
- UI cleanup
- Edge-case handling
- Documentation
- Final testing

---

# Out of Scope

Do NOT modify

- AST Engine
- Detection Rules
- Bandit Integration
- Semgrep Integration
- Safety Integration
- pip-audit Integration
- Authentication
- Reports Architecture
- REST API
- Docker
- Repository Explorer
- AI Features

Unless explicitly requested.

---

# Verification Checklist

Every completed sprint must satisfy

☐ Django starts successfully

☐ No Python errors

☐ Existing scans still work

☐ Existing reports still generate

☐ Existing dashboard functionality preserved

☐ Existing authentication preserved

☐ Responsive layout maintained

☐ Accessibility preserved

☐ No backend regressions

☐ Existing scanners continue working

☐ Progress states update correctly

---

# Commit Strategy

One sprint = One commit

Examples

feat(scan): add live scan progress

feat(scan): implement engine progress tracking

feat(scan): improve scan lifecycle

feat(scan): enhance rescan workflow

feat(scan): redesign demo scan experience

feat(scan): add live scan console

feat(ui): add scan notifications

feat(scan): improve scan history

feat(scan): add scan comparison

chore(scan): finalize scan experience

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
2. Verify existing scan functionality.
3. Verify reports continue working.
4. Verify responsive layout.
5. Verify no backend regressions.
6. Stop.

Never automatically continue to the next sprint.

Wait for the next prompt.