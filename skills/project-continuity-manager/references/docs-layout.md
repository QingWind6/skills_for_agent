# docs/agent Layout

Use `docs/agent/` as the durable memory layer for the repository. Keep long-lived facts near the top level and session-specific notes inside `handoffs/`.

## Directory Layout

```text
docs/agent/
├── README.md
├── START_HERE.md
├── PROJECT_STATUS.md
├── ARCHITECTURE.md
├── DECISIONS.md
├── TASKS.md
├── CONTEXT.md
└── handoffs/
    └── YYYY-MM-DD-HHMMSS-topic.md
```

## What Goes Where

### README.md

Purpose:
- Entry point for humans and agents
- Reading order
- Link map

Put here:
- Where to start
- Which files matter most
- High-level maintenance rules

Do not put here:
- Detailed architecture
- Session notes
- Backlog detail

### START_HERE.md

Purpose:
- Fast orientation in under five minutes

Put here:
- Project summary
- Core goal
- Tech stack
- Current phase
- What a new agent should read next

Do not let this become a second architecture document.

### PROJECT_STATUS.md

Purpose:
- Current truth of the project

Put here:
- Current phase
- Active task
- Current blockers
- Recently completed work
- Next work
- Files or areas currently in motion
- Path to the latest handoff

This is the most frequently updated file.

### ARCHITECTURE.md

Purpose:
- Stable explanation of how the system fits together

Put here:
- Major modules
- Data flow
- Boundaries and invariants
- Important dependencies
- Integration points

Update it only when the architecture meaningfully changes.

### DECISIONS.md

Purpose:
- Record why major choices were made

Put here:
- Decision title
- Date
- Context
- Options considered
- Decision
- Consequences

Use short ADR-style entries. If a decision is reversed, add a new entry instead of hiding history.

### TASKS.md

Purpose:
- Medium-term backlog with priority and acceptance criteria

Put here:
- Now / Next / Later groupings
- Owner if relevant
- Acceptance criteria
- Dependencies between tasks

Do not mix tiny session notes into this file.

### CONTEXT.md

Purpose:
- Durable technical notes that help future agents

Put here:
- Debugging notes worth preserving
- Research findings
- Important commands
- Environment quirks
- Known gotchas

Keep it high signal. If a note is obsolete, remove or mark it stale.

### handoffs/

Purpose:
- Session-level bridge from one agent to the next

Each handoff should contain:
- What changed in this session
- What the next agent should do first
- Relevant files
- Risks, blockers, and assumptions

A handoff is not the permanent system memory. Important facts must graduate into the top-level docs.

## Recommended Reading Order

### New agent on a long project

1. `START_HERE.md`
2. `PROJECT_STATUS.md`
3. `TASKS.md`
4. `ARCHITECTURE.md`
5. `DECISIONS.md`
6. `CONTEXT.md`
7. The newest relevant handoff in `handoffs/`

### Agent resuming a very specific paused task

1. `PROJECT_STATUS.md`
2. Latest relevant handoff
3. `TASKS.md`
4. Relevant code
5. `ARCHITECTURE.md` or `DECISIONS.md` if the task touches system design

## Conflict Resolution Rule

When code, docs, and handoffs disagree:

1. Verify actual code and tests.
2. Decide what the truth is now.
3. Update `PROJECT_STATUS.md` first.
4. Update any stable docs that should keep the same truth.
5. Mention the correction in the next handoff if it affected current work.
