# Agent Docs Hub - {{PROJECT_NAME}}

This directory is the shared memory layer for the project. Every new agent should use it before making non-trivial changes.

## Read Order

### First time in the project

1. `START_HERE.md`
2. `PROJECT_STATUS.md`
3. `TASKS.md`
4. `ARCHITECTURE.md`
5. `DECISIONS.md`
6. `CONTEXT.md`
7. the newest relevant file in `handoffs/`

### Fast resume

1. `PROJECT_STATUS.md`
2. latest relevant handoff in `handoffs/`
3. `TASKS.md`
4. any design doc needed for the task

## Maintenance Rules

- `PROJECT_STATUS.md` is the current source of truth.
- `handoffs/` stores session-level notes, not permanent truth.
- If architecture changes, update `ARCHITECTURE.md`.
- If a decision matters later, record it in `DECISIONS.md`.
- If backlog order changes, update `TASKS.md`.
- If docs and code disagree, verify the code and then fix the docs.

## Session Exit Rule

Before ending a meaningful session:

1. Update `PROJECT_STATUS.md`.
2. Update any stable docs affected by the work.
3. Create a new handoff in `handoffs/`.
4. Validate the handoff.

## Directory Map

- `START_HERE.md`: fast orientation
- `PROJECT_STATUS.md`: current phase, active work, blockers, latest handoff
- `ARCHITECTURE.md`: system shape and invariants
- `DECISIONS.md`: technical decision log
- `TASKS.md`: prioritized backlog
- `CONTEXT.md`: durable technical notes and commands
- `handoffs/`: one file per meaningful pause or session stop
