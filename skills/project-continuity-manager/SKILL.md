---
name: project-continuity-manager
description: Maintain a durable `docs/agent/` memory system for large software projects that span many sessions, pauses, and agent or model handoffs. Use when bootstrapping a long-running project, resuming from prior agent docs, creating or validating a session handoff, or keeping status, architecture, decisions, and tasks aligned across multiple agents.
---

# Project Continuity Manager

Use `docs/agent/` as the shared memory layer for a long-running project. The goal is that a fresh agent can read a small set of files, understand the real project state, and continue safely without repeating work or fighting stale assumptions.

## When to Use

Use this skill when any of the following are true:

- The project is large enough that one chat session is not enough.
- Different agents or models may continue the same repository over time.
- The user says things like "resume", "continue from last time", "save state", "create handoff", or "read docs/agent".
- The project already has `docs/agent/` and the work should follow it.
- The agent is about to pause after a meaningful chunk of work and needs to leave a reliable handoff.

## Shared Source of Truth

Use this priority order when information disagrees:

1. Code, tests, and runnable behavior describe the real system.
2. `docs/agent/PROJECT_STATUS.md` is the source of truth for current work.
3. `docs/agent/ARCHITECTURE.md` and `docs/agent/DECISIONS.md` explain design and rationale.
4. `docs/agent/TASKS.md` describes the medium-term backlog.
5. `docs/agent/handoffs/*.md` are tactical per-session notes and must agree with `PROJECT_STATUS.md`.

If the docs disagree with the code, inspect the code, resolve the discrepancy, and update the docs before moving on.

## Quick Start

### Initialize a project memory layer

```bash
python3 scripts/init_project_docs.py \
  --project-dir /path/to/project \
  --project-name "MyProject" \
  --description "What the project is for" \
  --tech-stack "TypeScript,Next.js,PostgreSQL" \
  --primary-goal "Ship the first beta"
```

### Check that project docs are healthy

```bash
python3 scripts/check_project_docs.py --project-dir /path/to/project
```

### Create an end-of-session handoff

```bash
python3 scripts/create_handoff.py \
  --project-dir /path/to/project \
  --slug auth-refactor
```

### Validate a handoff before ending the session

```bash
python3 scripts/validate_handoff.py \
  /path/to/project/docs/agent/handoffs/2026-03-10-180000-auth-refactor.md
```

### Check whether an older handoff is still safe to trust

```bash
python3 scripts/check_handoff_freshness.py \
  /path/to/project/docs/agent/handoffs/2026-03-10-180000-auth-refactor.md
```

## Workflow

### 1. Session Start

If `docs/agent/` exists:

1. Read `docs/agent/START_HERE.md`.
2. Read `docs/agent/PROJECT_STATUS.md`.
3. Read `docs/agent/TASKS.md` if you need backlog context.
4. Read `docs/agent/ARCHITECTURE.md`, `docs/agent/DECISIONS.md`, and `docs/agent/CONTEXT.md` only as needed.
5. If resuming from a specific handoff, read that handoff completely and run `check_handoff_freshness.py` first when there has been a long gap or significant code churn.

If `docs/agent/` does not exist and the project is clearly long-running, initialize it first with `init_project_docs.py`.

### 2. Before Writing Code

- Confirm the active task in `PROJECT_STATUS.md`.
- If the current task is missing or outdated, update `PROJECT_STATUS.md` before coding.
- If the work changes scope, update `TASKS.md` and, when architecture changes, update `ARCHITECTURE.md` or `DECISIONS.md`.

### 3. During the Session

- Keep `PROJECT_STATUS.md` aligned with reality.
- Record durable architectural choices in `DECISIONS.md`, not only in the handoff.
- Put debugging commands, experiments, and gotchas in `CONTEXT.md` only if they will help a future agent.
- Prefer small, testable chunks and update the docs when the direction changes, not only at the end.

### 4. Session End

Before ending a substantial session:

1. Update `PROJECT_STATUS.md` with current state, blockers, next work, and touched files.
2. Update `TASKS.md` if backlog order or scope changed.
3. Update `ARCHITECTURE.md` or `DECISIONS.md` if the design changed.
4. Create a new handoff in `docs/agent/handoffs/`.
5. Validate the handoff with `validate_handoff.py`.
6. Make sure the latest handoff path is recorded in `PROJECT_STATUS.md`.

## Document Roles

- `README.md`: navigation hub for humans and agents.
- `START_HERE.md`: fast project orientation.
- `PROJECT_STATUS.md`: current phase, active work, blockers, and latest handoff.
- `ARCHITECTURE.md`: stable mental model of the system.
- `DECISIONS.md`: ADR-style record of technical choices and reversals.
- `TASKS.md`: prioritized backlog and acceptance criteria.
- `CONTEXT.md`: durable debugging notes, research, commands, and gotchas.
- `handoffs/*.md`: session snapshots with immediate next steps.

Read `references/docs-layout.md` when deciding what belongs in each file. Read `references/session-rhythm.md` when you need the detailed start, mid-session, or end-of-session checklist.

## Handoff Rules

- One meaningful pause should produce one handoff file.
- Name handoffs with a timestamp and a short slug.
- A handoff should capture what changed, what matters, and what the next agent should do first.
- Do not put secrets, tokens, passwords, or raw credentials in any handoff.
- Handoffs are tactical; if a fact should remain true for days or weeks, also copy it into the stable docs.

## Resources

- `scripts/init_project_docs.py`: bootstrap `docs/agent/` from reusable templates.
- `scripts/check_project_docs.py`: verify required docs exist and are still aligned.
- `scripts/create_handoff.py`: generate a timestamped handoff scaffold in `docs/agent/handoffs/`.
- `scripts/validate_handoff.py`: check completeness, referenced files, and accidental secrets.
- `scripts/check_handoff_freshness.py`: compare a handoff against current repo state.
- `references/docs-layout.md`: file-by-file guidance for the `docs/agent/` tree.
- `references/session-rhythm.md`: practical workflow for start, during, and end of session.
- `assets/templates/`: markdown templates used by the bootstrap and handoff scripts.
